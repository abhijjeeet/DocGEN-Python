from app import create_app, db
from app.models import User
from create_templates import create_defaults
import os

app = create_app()

# Auto-create tables and seed a default admin
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', is_admin=True)
        admin.set_password('password123')
        db.session.add(admin)
        db.session.commit()
        print("Created default admin: admin / password123")
    create_defaults()

if __name__ == '__main__':
    # Listen on 0.0.0.0 so Docker’s port mapping and external traffic can reach it
    app.run(host='0.0.0.0', port=5000, debug=True)
