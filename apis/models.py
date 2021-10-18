from flask_restx import Model, fields


user_model = Model('User', {
    'id': fields.Integer(readonly=True, description='Identificador único do usuário'),
    'email': fields.String(required=True, description='E-mail do usuário')
})

post_model = Model('Post', {
    'id': fields.Integer(readonly=True, description='Identificador único do post'),
    'title': fields.String(required=True, description='Título do post'),
    'body': fields.String(required=True, description='Corpo do post em Markdown'),
    'user': fields.Nested(user_model, description='Criador do post')
})

comment_model = Model('Comment', {
    'id': fields.Integer(readonly=True, description='Identificador único do comentário'),
    'body': fields.String(required=True, description='Corpo do comentário'),
    'user': fields.Nested(user_model, required=True, description='Criador do comentário'),
    'post': fields.Nested(post_model, required=True, description='Post comentado')
})

deleted_comment_model = Model('Comment', {
    'id': fields.Integer(readonly=True, description='Identificador único do comentário'),
    'body': fields.String(required=True, description='Corpo do comentário'),
    'post_id': fields.Integer(readonly=True, description='Identificador único do post'),
})

_post_comment_model = Model('PostComment', {
    'id': fields.Integer(readonly=True, description='Identificador único do comentário'),
    'body': fields.String(required=True, description='Corpo do comentário'),
    'user': fields.Nested(user_model, required=True, description='Criador do comentário')
})

commented_post_model = Model('CommentedPost', {
    'id': fields.Integer(readonly=True, description='Identificador único do post'),
    'title': fields.String(required=True, description='Título do post'),
    'body': fields.String(required=True, description='Corpo do post em Markdown'),
    'user': fields.Nested(user_model, description='Criador do post'),
    'comments': fields.List(fields.Nested(_post_comment_model), description='Comentários do post')
})

_album_photo_model = Model('AlbumPhoto', {
    'id': fields.Integer(readonly=True, description='Identificador único da foto'),
    'title': fields.String(required=True, description='título da foto'),
    'file': fields.String()
})

album_model = Model('Album', {
    'id': fields.Integer(readonly=True, description='Identificador único do álbum'),
    'name': fields.String(required=True, description='Nome do álbum de fotos'),
    'user': fields.Nested(user_model, description='Dono do álbum'),
    'photos': fields.List(fields.Nested(_album_photo_model), description='Fotos do álbum')
})

album_description_model = Model('Album', {
    'id': fields.Integer(readonly=True, description='Identificador único do álbum'),
    'name': fields.String(required=True, description='Nome do álbum de fotos'),
    'user': fields.Nested(user_model, description='Dono do álbum')
})
