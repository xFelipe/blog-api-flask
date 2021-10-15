from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from schemas import UserSchema
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return self.username

    def __init__(self, username, password):
        user_already_exists = self.query.filter_by(username=username).count()
        if user_already_exists:
            raise ValidationError('User already exists')
        valid_data = UserSchema().load(
            {'username': username, 'password': password}
        )
        self.username = valid_data['username']
        self.password = generate_password_hash(valid_data['password'])
