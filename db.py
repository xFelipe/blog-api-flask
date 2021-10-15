from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from sqlalchemy.orm import backref
from schemas import UserSchema
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

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


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    comments = db.relationship('Comment', backref='post', lazy='dynamic')


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'), nullable=False)
