import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    BCRYPT_LOG_ROUNDS = 13
    ACCESS_TOKEN_EXPIRATION = 900  # 15 minutes
    REFRESH_TOKEN_EXPIRATION = 2592000  # 30 days


def get_db_uri():
    """Construct database URI from environment variables"""
    db_type = os.getenv('DB_TYPE', 'mysql')
    if db_type == 'sqlite':
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(os.path.dirname(basedir), 'instance')
        os.makedirs(db_path, exist_ok=True)
        return f"sqlite:///{os.path.join(db_path, 'users_dev.db')}"
    
    # MySQL configuration for AWS RDS
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    
    if all([db_user, db_pass, db_host, db_name]):
        return f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}?charset=utf8mb4"
    
    # Fallback to local SQLite if AWS RDS credentials are not set
    return "sqlite:///local_dev.db"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_db_uri()
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = get_db_uri()
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Ensure required production settings are set
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production environment")
