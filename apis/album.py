from flask_restx.namespace import Namespace
from flask import request
from flask_restx import Resource
from core import db
from schemas import AlbumSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest
from apis.helpers import validate, save, delete
from apis.models import (user_model, album_model, album_description_model, _album_photo_model)


ns = Namespace('album', 'Operações em album de fotos')

ns.add_model('User', user_model)
ns.add_model('Album', album_model)
ns.add_model('AlbumDescription', album_description_model)
ns.add_model('AlbumPhoto', _album_photo_model)


@ns.route('')
class Album(Resource):
    @jwt_required()
    @ns.marshal_with(album_model, code=201, envelope='album')
    def post(self):
        user = db.User.query.get(get_jwt_identity())
        request_data = validate(request.get_json(), AlbumSchema())
        new_album = db.Album(user=user, **request_data)
        return save(new_album)

    @ns.marshal_list_with(album_description_model, code=200, envelope='albums')
    def get(self):
        return db.Album.query.all()


@ns.route('/<int:album_id>')
@ns.doc(response={404: 'Album não encontrado'}, params={'album_id': 'O id do álbum'} )
class TargetAlbum(Resource):
    """Consulta, altera ou deleta post"""
    @ns.marshal_with(album_model, code=200, envelope='album')
    def get(self, album_id):
        album = db.Album.get_or_404(album_id)
        return album

    @jwt_required()
    @ns.marshal_with(album_model, code=200, envelope='album')
    def delete(self, album_id):
        album = db.Album.get_or_404(album_id)
        current_user_id = get_jwt_identity()
        if current_user_id != album.user.id:
            raise BadRequest('Apenas o criador do álbum pode apagá-lo')

        return delete(album)
