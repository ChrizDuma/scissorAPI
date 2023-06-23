from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_cors import CORS
from flask_caching import Cache


authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize",
        }
    }


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api(title="URL Shortening API",
        description="API for URL shortening",
        authorizations=authorizations,
        security="Bearer Auth")
cors = CORS()
cache = Cache(config={"CACHE_TYPE": "simple"})

