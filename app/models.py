from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager
from sqlalchemy.dialects.sqlite import JSON  # if you’re on Postgres, use from sqlalchemy import JSON

class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    daily_count   = db.Column(db.Integer, default=0)
    last_date     = db.Column(db.Date, default=date.today)
    is_admin      = db.Column(db.Boolean, default=False)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def can_generate(self):
        if self.last_date != date.today():
            self.daily_count = 0
            self.last_date = date.today()
        return self.daily_count < 3

    def record_generation(self):
        if self.last_date != date.today():
            self.daily_count = 0
            self.last_date = date.today()
        self.daily_count += 1
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Template(db.Model):
    """
    Stores each document template uploaded via the Admin UI.
    - slug: used in URLs (/generate/<slug>)
    - name: human‐readable label
    - docx_path: filename under app/doc_templates/
    - txt_path:  filename under app/doc_templates/
    - html_path: optional, for PDF snippets
    - fields:    JSON list of {name,label,type} dicts for dynamic WTForms
    """
    id        = db.Column(db.Integer, primary_key=True)
    slug      = db.Column(db.String(80), unique=True, nullable=False)
    name      = db.Column(db.String(120), nullable=False)
    docx_path = db.Column(db.String(200), nullable=False)
    txt_path  = db.Column(db.String(200), nullable=True)
    html_path = db.Column(db.String(200), nullable=True)
    fields    = db.Column(JSON, nullable=False)
    category  = db.Column(db.String(80), nullable=False, default='General')
    region    = db.Column(db.String(80), nullable=True)
