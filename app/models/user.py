import uuid
from datetime import datetime

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')
        self.admin = False
        self.public_id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @property
    def acess_token(self):
        return create_access_token(
            identity=self.public_id,
            additional_claims={
                'admin': self.admin,
                'username': self.username,
            },
        )

    @property
    def refresh_token(self):
        return create_refresh_token(identity=self.public_id)

    @staticmethod
    def check_exists(username):
        return Users.query.filter_by(username=username).first() is not None

    @staticmethod
    def check_password(username, password):
        user = Users.query.filter_by(username=username).first()
        if user is None:
            return None
        if check_password_hash(user.password, password):
            return user
        return None

    @staticmethod
    def login_jwt(username, password):
        if user := Users.check_password(username, password):
            return {
                'acess_token': user.acess_token,
                'refresh_token': user.refresh_token,
                'token_type': 'bearer',
            }
        return None

    @staticmethod
    def refresh_jwt(identity):
        user = Users.query.filter_by(public_id=identity).first()
        return {
            'acess_token': user.acess_token,
            'token_type': 'bearer',
        }
