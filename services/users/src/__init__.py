import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)
    
    # Set configuration directly
    app.config.from_object('src.config.DevelopmentConfig')
    
    # Override with environment variables if they exist
    if os.getenv('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    if os.getenv('SECRET_KEY'):
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    print(f"SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Configure CORS
    cors.init_app(app, resources={
        r"/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Import and register blueprints
    from src.api import api
    api.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}
        
    return app

    return app
