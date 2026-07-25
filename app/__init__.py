import os
from flask import Flask, g, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

    db.init_app(app)

    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from flask import g

    @app.before_request
    def load_logged_in_user():
        from app.models import User
        user_id = session.get('user_id')
        g.user = User.query.get(user_id) if user_id else None

    return app




