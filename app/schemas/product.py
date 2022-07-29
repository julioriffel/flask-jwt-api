from flask_rebar import RequestSchema
from flask_rebar import ResponseSchema
from marshmallow import fields
from marshmallow import pre_dump
from marshmallow import pre_load


class ProductRequestSchema(RequestSchema):
    name = fields.String(required=True)
    quantity = fields.Integer(required=True)
    price = fields.Float(required=True)
    description = fields.String(required=True)


class ProductRequestPatchSchema(RequestSchema):
    name = fields.String()
    quantity = fields.Integer()
    price = fields.Float()
    description = fields.String()


class ProductSchema(ResponseSchema):
    id = fields.Integer()
    name = fields.String()
    quantity = fields.Integer()
    price = fields.Float()
    description = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class ProductListSchema(ResponseSchema):
    data = fields.Nested(ProductSchema, many=True)

    @pre_dump
    @pre_load
    def envelope_in_data(self, data, **kwargs):
        if type(data) is not dict or 'data' not in data.keys():
            return {'data': data}
        else:
            return data
