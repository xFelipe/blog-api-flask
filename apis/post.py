from flask_restx.namespace import Namespace
from flask import request
from flask_restx import Resource
from core import db
from schemas import PostSchema, ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest
from flask_restx import fields


ns = Namespace('post', 'Operações em blogpost')

user_model = ns.model('User', {
    'id': fields.Integer(readonly=True, description='Identificador único do usuário'),
    'email': fields.String(required=True, description='E-mail do usuário')
})
post_model = ns.model('Post', {
        'id': fields.Integer(readonly=True, description='Identificador único do post'),
        'title': fields.String(required=True, description='Título do post'),
        'body': fields.String(required=True, description='Corpo do post'),
        'user': fields.Nested(user_model, description='Criador do post')
})

@ns.route('/<int:post_id>')
@ns.doc(response={404: 'Post não encontrado'}, params={'post_id': 'O id do post'} )
class TargetPost(Resource):
    """Consulta, altera ou deleta post"""
    @ns.marshal_with(post_model, code=200, envelope='post')
    def get(self, post_id):
        return db.Post.query.get_or_404(
            post_id,
            description=f'Não foi possível localizar o post com id {post_id}'
        )

    @jwt_required()
    @ns.marshal_with(post_model, code=200, envelope='post')
    def delete(self, post_id):
        post = db.Post.query.get_or_404(
            post_id,
            description=f'Não foi possível localizar o post com id {post_id}'
        )
        current_user_id = get_jwt_identity()
        if current_user_id != post.user.id:
            raise BadRequest('Apenas o criador do post pode apaga-lo')

        session = db.db.session()
        session.delete(post)
        session.commit()
        return post


@ns.route('')
class Post(Resource):
    @jwt_required()
    @ns.marshal_with(post_model, code=201, envelope='post')
    def post(self):
        user = db.User.query.get(get_jwt_identity())
        try:
            request_data = PostSchema().load(request.get_json())
        except ValidationError as validation_error:
            e = BadRequest(validation_error.messages)
            e.data = {
                'message': 'Erro de validação.',
                'errors': validation_error.messages
            }
            raise e
        new_post = db.Post(user=user, **request_data)
        session = db.db.session()
        session.add(new_post)
        session.commit()
        return new_post

    @ns.marshal_list_with(post_model, code=200, envelope='posts')
    def get(self):
        return db.Post.query.all()
