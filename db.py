from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from schemas import UserSchema
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return self.email

    def __init__(self, email, password):
        user_already_exists = self.query.filter_by(email=email).count()
        if user_already_exists:
            raise ValidationError('User already exists')
        valid_data = UserSchema().load(
            {'email': email, 'password': password}
        )
        self.email = valid_data['email']
        self.password = generate_password_hash(valid_data['password'])
