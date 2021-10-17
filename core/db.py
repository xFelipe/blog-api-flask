from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from schemas import UserSchema
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    posts = db.relationship('Post', backref='user', lazy='dynamic', cascade='all,delete')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    albuns = db.relationship('Album', backref='user', lazy='dynamic', cascade='all,delete')

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

    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all,delete')
    
    @classmethod
    def get_or_404(cls, post_id):
        return cls.query.get_or_404(
            post_id,
            description=f'Não foi possível localizar o post com id {post_id}'
        )


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'), nullable=False)


    @classmethod
    def get_or_404(cls, post_id):
        return cls.query.get_or_404(
            post_id,
            description=f'Não foi possível localizar o comentário com id {post_id}'
        )

class Album(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    photos = db.relationship('Photo', backref='album', lazy='dynamic', cascade='all,delete')


class Photo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    file_name = db.Column(db.String(255), nullable=False)
    file = db.Column(db.LargeBinary(), nullable=False)
    album_id = db.Column(db.Integer(), db.ForeignKey('album.id'), nullable=False)
