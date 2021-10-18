from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, fields
from flask_restx import Resource
from werkzeug.exceptions import BadRequest
from apis.helpers import delete, validate, save
from apis.models import user_model, post_model, comment_model, deleted_comment_model
from schemas import CommentSchema
from core import db


ns = Namespace('comment', 'Comentários em post')

ns.add_model('User', user_model)
ns.add_model('Comment', comment_model)
ns.add_model('DeletedComment', deleted_comment_model)


@ns.route('')
class Comment(Resource):
    @ns.marshal_list_with(comment_model, code=200, envelope='comments')
    def get(self):
        return db.Comment.query.all()

    @jwt_required()
    @ns.marshal_with(comment_model, code=201, envelope='comment')
    def post(self):
        data = validate(request.get_json(), CommentSchema())
        post_id = data['post_id']
        post = db.Post.get_or_404(post_id)
        current_user = db.User.query.get(get_jwt_identity())
        new_comment = db.Comment(
            body = data['body'],
            user = current_user,
            post = post
        )
        return save(new_comment)


@ns.route('/<int:comment_id>')
class TargetComment(Resource):
    @ns.marshal_with(comment_model, code=200, envelope='comment')
    def get(self, comment_id):
        return db.Comment.get_or_404(comment_id)

    @jwt_required()
    @ns.marshal_with(deleted_comment_model, code=200, envelope='comment')
    def delete(self, comment_id):
        comment = db.Comment.get_or_404(comment_id)
        current_user_id = get_jwt_identity()
        if current_user_id != comment.user.id:
            raise BadRequest('Apenas o criador do post pode apagá-lo')
        return delete(comment)
