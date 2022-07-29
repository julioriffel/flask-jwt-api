from marshmallow import fields
from marshmallow import Schema


class HealthSchema(Schema):
    status = fields.String()
