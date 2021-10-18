from flask import request, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace
from flask_restx import Resource
from werkzeug.exceptions import BadRequest
from apis.helpers import delete, validate, save, save_image_as_jpeg
from apis.models import user_model, photo_model, album_description_model
from schemas import PhotoSchema
from core import db
import os


ns = Namespace('photo', 'Fotos de um álbum')

ns.add_model('User', user_model)
ns.add_model('Photo', album_description_model)
ns.add_model('Photo', photo_model)


@ns.route('')
class Photo(Resource):
    @ns.marshal_list_with(photo_model, code=200, envelope='photos')
    def get(self):
        return db.Photo.query.all()

    @jwt_required()
    @ns.marshal_with(photo_model, code=201, envelope='photo')
    def post(self):
        valid_data = validate(request.form, PhotoSchema())
        image = request.files.get('image')
        if not image:
            error = BadRequest('Validation error')
            error.data = {
                'message': 'Erro de validação.',
                'errors': {'image': 'Necessário enviar arquivo de imagem neste campo obrigatório.'}
            }
            raise error
        album_id = valid_data['album_id']
        album = db.Album.get_or_404(album_id)
        if album.user_id != get_jwt_identity():
            return BadRequest('Só é possível inserir fotos em álbuns do próprio usuário')
        file_name = save_image_as_jpeg(
            image,
            current_app.config['PHOTO_FOLDER_PATH']
        )
        new_photo = db.Photo(
            title = valid_data['title'],
            file_name = file_name,
            album = album
        )
        return save(new_photo)


@ns.route('/<int:photo_id>')
class TargetPhoto(Resource):
    @ns.marshal_with(photo_model, code=200, envelope='photo')
    def get(self, photo_id):
        return db.Photo.get_or_404(photo_id)

    @jwt_required()
    @ns.marshal_with(photo_model, code=200, envelope='comment')
    def delete(self, photo_id):
        photo = db.Photo.get_or_404(photo_id)
        current_user_id = get_jwt_identity()
        if current_user_id != photo.album.user.id:
            raise BadRequest('Apenas o criador da foto pode apagá-la')
        photo_file_path = os.path.join(
            current_app.config['PHOTO_FOLDER_PATH'], photo.file_name
        )
        delete(photo)
        os.remove(photo_file_path)
        return photo
