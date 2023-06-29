from decouple import config
from datetime import timedelta
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

db_name = "file.db"

default_uri = "postgres://{}:{}@{}/{}".format(
    "postgres", "password", "localhost:5432", db_name
)


uri = os.environ.get("DATABASE_URL", default=default_uri)
# uri = os.getenv("DATABASE_URL", default_uri)
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)



cache_url = os.getenv("CACHE_REDIS_URL")


class Config:
    # secret key for app
    SECRET_KEY = config("SECRET_KEY", "my_secret_key😉")
    # secret key for jwt access
    JWT_SECRET_KEY = config("JWT_SECRET_KEY", "secret🔐")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # JWT_BLACKLIST_ENABLED = True
    # JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300

class Dev_config(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")


class Test_config(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class Prod_config(Config):
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = config("DEBUG", False, cast=bool)
    CACHE_TYPE = "Redis"
    CACHE_REDIS_URL = cache_url

# Configuration Dictionary for representation
# --------------------------------------------
config_dict = {"dev": Dev_config, "test": Test_config, "prod": Prod_config}
# ---------------------------------------------
