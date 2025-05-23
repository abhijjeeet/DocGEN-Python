import os
from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, current_app, request
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Template
from app.forms import TemplateCreateForm
from jinja2 import TemplateSyntaxError, UndefinedError
from docxtpl import DocxTemplate

admin_bp = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin',
    template_folder='templates/admin'
)

def admin_required(fn):
    """Decorator: only allow users with is_admin=True."""
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            flash("Admin access only.", "warning")
            return redirect(url_for('main.dashboard'))
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@admin_bp.route('/templates')
@admin_required
def list_templates():
    templates = Template.query.all()
    return render_template('list.html', templates=templates)


@admin_bp.route('/templates/new', methods=['GET','POST'])
@admin_required
def new_template():
    form = TemplateCreateForm()

    # 1) pull existing categories for the datalist
    existing = (
        db.session
          .query(Template.category)
          .distinct()
          .order_by(Template.category)
          .all()
    )
    categories = [c[0] for c in existing if c[0]]

    # placeholder for any syntax‐error guidelines
    guidelines = None

    if form.validate_on_submit():
        slug     = secure_filename(form.slug.data)
        name     = form.name.data
        category = form.category.data.strip()

        existing = Template.query.filter_by(slug=slug).first()
        if existing:
            form.slug.errors.append("This slug is already in use. Please choose a different one.")
            return render_template("admin/new.html", form=form)


        upload_dir = os.path.join(current_app.root_path, 'doc_templates')
        os.makedirs(upload_dir, exist_ok=True)

        docx_fname = f"{slug}_template.docx"
        dest_path  = os.path.join(upload_dir, docx_fname)

        try:
            # save the uploaded file
            form.docx_file.data.save(dest_path)

            # attempt to parse it and extract placeholders
            tpl = DocxTemplate(dest_path)
            placeholders = tpl.get_undeclared_template_variables()

        except (TemplateSyntaxError, UndefinedError) as e:
            # remove bad file
            if os.path.exists(dest_path):
                os.remove(dest_path)
            guidelines = (
                f"<strong>Template syntax error:</strong> {e}<br>"
                "• Make sure all variables are valid Python identifiers, e.g. "
                "<code>{{&#123; my_var &#125;}}</code><br>"
                "• Do not include spaces or invalid characters inside your <code>{{…}}</code> tags."
            )
        except Exception as e:
            if os.path.exists(dest_path):
                os.remove(dest_path)
            guidelines = f"<strong>Failed to process template:</strong> {e}"

        if not guidelines:
            # no errors, safe to create the DB record
            fields = [
                {"name": ph,
                 "label": ph.replace('_',' ').title(),
                 "type": "StringField"}
                for ph in placeholders
            ]

            new = Template(
                slug=slug,
                name=name,
                category=category,
                docx_path=docx_fname,
                fields=fields
            )
            db.session.add(new)
            db.session.commit()

            flash(f"Template '{name}' created!", "success")
            return redirect(url_for('admin.list_templates'))

    # either GET or a validation / syntax error: re-render the form
    return render_template(
        'new.html',
        form=form,
        categories=categories,
        guidelines=guidelines
    )

@admin_bp.route('/templates/<int:template_id>/delete', methods=['POST'])
@login_required
def delete_template(template_id):
    tmpl = Template.query.get_or_404(template_id)

    # delete associated files from disk
    for attr in ('docx_path', 'txt_path', 'html_path'):
        path = getattr(tmpl, attr, None)
        if path:
            full = os.path.join(current_app.root_path, 'doc_templates', path)
            if os.path.exists(full):
                os.remove(full)

    db.session.delete(tmpl)
    db.session.commit()
    flash(f"Template “{tmpl.name}” has been deleted.", "success")
    return redirect(url_for('admin.list_templates'))
