from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class)

    db.init_app(app)

    from .routes.public import public_bp
    from .routes.admin import admin_bp  # Now imports from admin package
    from .routes.auth import auth_bp
    from .routes.admin.api_docs import get_swagger_blueprint

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Register Swagger UI blueprint
    swagger_bp = get_swagger_blueprint()
    app.register_blueprint(swagger_bp)

    return app
