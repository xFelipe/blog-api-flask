from flask_restx.namespace import Namespace
from flask import request
from flask_restx import Resource
from core import db
from schemas import PostSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest
from apis.helpers import validate, save, delete
from apis.models import (user_model, comment_model, _post_comment_model,
                         commented_post_model, post_model)


ns = Namespace('post', 'Operações em blogpost')

ns.add_model('User', user_model)
ns.add_model('Comment', comment_model)
ns.add_model('Post', post_model)
ns.add_model('CommentedPost', commented_post_model)
ns.add_model('PostComment', _post_comment_model)


@ns.route('')
class Post(Resource):
    @jwt_required()
    @ns.marshal_with(post_model, code=201, envelope='post')
    def post(self):
        user = db.User.query.get(get_jwt_identity())
        request_data = validate(request.get_json(), PostSchema())
        new_post = db.Post(user=user, **request_data)
        save(new_post)
        return new_post

    @ns.marshal_list_with(post_model, code=200, envelope='posts')
    def get(self):
        return db.Post.query.all()


@ns.route('/<int:post_id>')
@ns.doc(response={404: 'Post não encontrado'}, params={'post_id': 'O id do post'} )
class TargetPost(Resource):
    """Consulta, altera ou deleta post"""
    @ns.marshal_with(commented_post_model, code=200, envelope='post')
    def get(self, post_id):
        post = db.Post.get_or_404(post_id)
        return post

    @jwt_required()
    @ns.marshal_with(post_model, code=200, envelope='post')
    def delete(self, post_id):
        post = db.Post.get_or_404(post_id)
        current_user_id = get_jwt_identity()
        if current_user_id != post.user.id:
            raise BadRequest('Apenas o criador do post pode apagá-lo')

        return delete(post)
