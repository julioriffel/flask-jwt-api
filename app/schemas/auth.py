from flask_rebar import RequestSchema
from marshmallow import fields


class UserRequestSchema(RequestSchema):
    username = fields.String(required=True)
    password = fields.String(required=True)
