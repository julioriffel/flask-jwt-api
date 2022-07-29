from flask_jwt_extended import jwt_required
from flask_rebar import errors

from app.app import db
from app.app import rebar
from app.app import registry
from app.models.product import Product
from app.schemas.product import ProductListSchema
from app.schemas.product import ProductRequestPatchSchema
from app.schemas.product import ProductRequestSchema
from app.schemas.product import ProductSchema


@registry.handles(
    rule='/products',
    method='GET',
    tags=['products'],
    response_body_schema={200: ProductListSchema()},
)
@jwt_required()
def get_products():
    products = Product.query.all()
    return products


@registry.handles(
    rule='/products/<int:pk>',
    method='GET',
    tags=['products'],
    response_body_schema={200: ProductSchema()},
)
@jwt_required()
def get_product(pk: int):
    product = Product.query.filter_by(id=pk).first()
    if not product:
        raise errors.NotFound()
    return product


@registry.handles(
    rule='/products',
    method='POST',
    request_body_schema=ProductRequestSchema(),
    tags=['todo'],
    response_body_schema={201: ProductSchema()},
)
@jwt_required()
def create_product():
    body = rebar.validated_body
    product = Product(**body)
    db.session.add(product)
    db.session.commit()
    return product, 201


@registry.handles(
    rule='/products/<int:pk>',
    method='PUT',
    request_body_schema=ProductRequestSchema(),
    tags=['product'],
    response_body_schema={200: ProductSchema()},
)
@jwt_required()
def put_product(pk):
    product = Product.query.filter_by(id=pk).first()
    if not product:
        raise errors.NotFound()
    params = rebar.validated_body
    product.update(**params)
    return product


@registry.handles(
    rule='/products/<int:pk>',
    method='PATCH',
    request_body_schema=ProductRequestPatchSchema(),
    tags=['product'],
    response_body_schema={200: ProductSchema()},
)
@jwt_required()
def patch_product(pk):
    product = Product.query.filter_by(id=pk).first()
    if not product:
        raise errors.NotFound()
    params = rebar.validated_body
    product.update(**params)
    return product


@registry.handles(
    rule='/products/<int:pk>',
    method='DELETE',
    tags=['product'],
    response_body_schema={204: None},
)
@jwt_required()
def delete_todo(pk):
    product = Product.query.filter_by(id=pk).first()
    if not product:
        raise errors.NotFound()
    product.delete()

    return None, 204
