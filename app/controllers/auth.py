from flask import jsonify
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from app.app import db
from app.app import rebar
from app.app import registry_auth
from app.models.user import Users
from app.schemas.auth import UserRequestSchema


@registry_auth.handles(
    rule='/register',
    method='POST',
    request_body_schema=UserRequestSchema(),
    tags=['user'],
)
def signup_user():
    body = rebar.validated_body
    if Users.check_exists(body.get('username')):
        return jsonify({'message': 'user already exists'}), 409
    new_user = Users(**body)
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'registration successfully'}


@registry_auth.handles(
    rule='/login',
    method='POST',
    tags=['user'],
)
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return {'Authentication': 'login required'}, 401
    jwt = Users.login_jwt(auth.username, auth.password)
    if jwt:
        return jwt, 200
    return {'Authentication': 'login required'}, 401


@registry_auth.handles(
    rule='/refresh',
    method='POST',
    tags=['user'],
)
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    jwt = Users.refresh_jwt(identity)
    if jwt:
        return jwt, 200
    return {'Authentication': 'login required'}, 401
