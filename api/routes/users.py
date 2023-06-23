from ..models import Url, User
from flask_restx import Namespace, abort, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import cache



users_ns = Namespace('users', 
               description="namespace for operations on users")

users_model = users_ns.model(
    'User',{
      'id' : fields.Integer(dump_only=True),
      'username' : fields.String(required=True),
      'first_name' : fields.String(required=True),
      'last_name' : fields.String(required=True),
      'email' : fields.String(required=True),
      'password' : fields.String(required=True, load_only=True),
      'confirm_password' : fields.String(load_only=True, required=True)
    }
)


# class UserDashboardSchema(UserSchema):
#     user_links = fields.Nested(GetLinksSchema(), many=True)
