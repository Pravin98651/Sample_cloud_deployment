import os


class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my_precious"
    BCRYPT_LOG_ROUNDS = 13
    ACCESS_TOKEN_EXPIRATION = 900  # 15 minutes
    REFRESH_TOKEN_EXPIRATION = 2592000  # 30 days


class DevelopmentConfig(BaseConfig):
    # Use SQLite database in the current directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(os.path.dirname(basedir), 'instance')
    os.makedirs(db_path, exist_ok=True)
    db_file = os.path.join(db_path, 'users_dev.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_file}"
    print(f"Using database at: {SQLALCHEMY_DATABASE_URI}")
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3


class ProductionConfig(BaseConfig):
    url = os.environ.get("DATABASE_URL")

    if url is not None and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = url
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
