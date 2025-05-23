# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

# db = SQLAlchemy()
# login_manager = LoginManager()

# def create_app():
#     app = Flask(
#         __name__,
#         static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
#         template_folder='templates'
#     )
#     app.config.from_object('app.config.Config')

#     # initialize extensions
#     db.init_app(app)
#     login_manager.init_app(app)
#     login_manager.login_view = 'auth.login'

#     # register the auth blueprint
#     from app.auth import auth_bp
#     app.register_blueprint(auth_bp, url_prefix='/auth')

#     # register the admin blueprint
#     from app.admin import admin_bp
#     app.register_blueprint(admin_bp, url_prefix='/admin')

#     # register the main blueprint
#     from app.main import main_bp
#     app.register_blueprint(main_bp)

#     @app.template_filter('datetimeformat')
#     def datetimeformat(value, fmt: str = "%Y-%m-%d %H:%M"):
#         if isinstance(value, (datetime,)):
#             return value.strftime(fmt)
#         return value  # if it’s already a str, or None

#     return app

import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
        template_folder='templates'
    )
    app.config.from_object('app.config.Config')
    csrf.init_app(app)
    # register extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # ==== register the datetimeformat filter ====
    @app.template_filter('datetimeformat')
    def datetimeformat(value, fmt: str = "%Y-%m-%d %H:%M"):
        if isinstance(value, datetime):
            return value.strftime(fmt)
        return value

    # register blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    from app.main import main_bp
    app.register_blueprint(main_bp)
    return app
