from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

from .extensions import migrate, jwt, api, cache, db
from .models import User, Link
from .utils.blacklist import BLACKLIST
from .config.config import config_dict
from .routes.url import short_namespace
from .auth.views import auth_namespace
from http import HTTPStatus


def create_app(config_app=config_dict["prod"]):

    app = Flask(__name__)
    app.config.from_object(config_app)

    load_dotenv()
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)


    api.add_namespace(auth_namespace,path="/auth")
    api.add_namespace(short_namespace, path="/shortme")

    # Enable CORS
    CORS(app, supports_credentials=True)
    cache.init_app(app)
    jwt.init_app(app)



    # ------------------------------------------------------------
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload['type'] in BLACKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {
            "message": "The token has been revoked",
            "error": "token_revoked"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            "message": "The token has expired",
            "error": "token_expired"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            "message": "Token verification failed",
            "error": "invalid_token"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            "message": "Request is missing an access token",
            "error": "authorization_required"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback():
        return {
            "message": "The token is not fresh",
            "error": "fresh_token_required"
        }, HTTPStatus.UNAUTHORIZED




    @app.shell_context_processor
    def make_shell_context():
        with app.app_context():
            db.create_all()

        return {"db": db, "User": User, "Link": Link}

    return app
