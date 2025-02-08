from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        from .routes import auth_routes, main_routes
        app.register_blueprint(auth_routes.auth_bp)
        app.register_blueprint(main_routes.main_bp)
        
        from .models import User, Course, Message
        db.create_all()
        
    return app