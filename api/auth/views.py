from flask_restx import Namespace, Resource, fields, abort
from ..models.users import User
from ..extensions import db
from ..utils.blacklist import BLACKLIST
from passlib.hash import pbkdf2_sha256 as sha256
from http import HTTPStatus
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jti,
)
import datetime
from datetime import timedelta
from ..extensions import cache

# from utils import db, RevokedToken


auth_namespace = Namespace("auth", description="Namespace for Authentication")


# --- serializers ---

# signup model
SignUp_Model = auth_namespace.model(
    "SignUp",
    {
        "username": fields.String(description="username", required=True),
        "first_name" : fields.String(required=True),
        "last_name" : fields.String(required=True),
        "email": fields.String(description="email", required=True),
        "password": fields.String(description="password", required=True),
        "confirm_password": fields.String(description="confirm user password")
    },
)

# user model
User_Model = auth_namespace.model(
    "User",
    {
        "id": fields.Integer(description="user id"),
        "username": fields.String(description="username"),
        "email": fields.String(description="email"),
        "password": fields.String(description="password hash"),
        "reg_date": fields.DateTime(description="registration date"),
        "link_history": fields.String(description="link_history"),
    },
)

# on login for registered user
Login_Model = auth_namespace.model(
    "Login",
    {
        "username": fields.String(required=True, description="username"),
        "password": fields.String(required=True, description="Password"),
    },
)


# --- routing ---


# signup
@auth_namespace.route("/signup")
class SignUp(Resource):
    @auth_namespace.expect(SignUp_Model, validate=True)
    @auth_namespace.marshal_with(User_Model)
    def post(self):
        data = auth_namespace.payload


        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        confirm_passwword = data.get('password')

        # Check if the username or email already exists
        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, HTTPStatus.CONFLICT

        if User.query.filter_by(email=email).first():
            return {"message": "Email already exists"}, HTTPStatus.CONFLICT

        if password != confirm_passwword:
            abort(400, message="Passwords do not match")

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=sha256.hash(password),
            reg_date=datetime.datetime.utcnow()
        )   
        user.save()

        return user, HTTPStatus.OK


# on Refresh
@auth_namespace.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user = get_jwt_identity()

        access_token = create_access_token(identity=user,expires_delta=timedelta(hours=2))

        return {"access_token": access_token}, HTTPStatus.OK


# Login
@auth_namespace.route("/login")
class Login(Resource):
    @auth_namespace.expect(Login_Model)
    def post(self):
        data = auth_namespace.payload

        username = data["username"]
        password = data["password"]

        current_user = User.query.filter_by(username=username).first()

        if not current_user:
            abort(400, message="not valid")

        if not sha256.verify(password, current_user.password):
            abort(401, message="Invalid password")

        access_token = cache.get(current_user.id)

        if not access_token:
            access_token = create_access_token(identity=current_user.id)
            cache.set(current_user.id, access_token, timeout=None)

        refresh_token = create_refresh_token(identity=current_user.id)

        response = {"access_token": access_token, "refresh_token": refresh_token}

        return response, HTTPStatus.OK

        # Consider a redirect after signup/login back to the landing page as a signed-up user
        # return redirect(url_for('index'))


# log_out
@auth_namespace.route("/logout", methods=["DELETE"])
class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jti()["jti"]
        current_user = get_jwt_identity()
        cached_data = cache.get(current_user)

        if cached_data:
            cache.delete(current_user)

            # Get the JWT ID and add it to the Blacklist

        BLACKLIST.add(jti)

        return {"message": "Successfully logged out"}, HTTPStatus.OK
