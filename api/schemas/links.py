# from ..routes.url import short_namespace
# from flask_restx import fields
from marshmallow import post_dump
from flask import request






# get_url_model = short_namespace.model(
#     "get_url_model",
#     {
#         "id": fields.Integer(),
#         "user_id": fields.Integer(),
#         "original_url": fields.String(),
#         "short_url": fields.String(),
#         "visits": fields.Integer(),
#         "date_created": fields.String()
#     }
# )


@post_dump(pass_many=True)
def add_host_url(self, data, many, **kwargs):
  host_url = request.host_url  # Get the host URL from the request
  if many:
    # If serializing multiple objects, update each object's short_url field
    for obj in data:
      obj['short_url'] = host_url + obj['short_url']
  else:
    # If serializing a single object, update its short_url field
    data['short_url'] = host_url + data['short_url']
    return data