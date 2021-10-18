from marshmallow import Schema, ValidationError
from werkzeug.exceptions import BadRequest
from core.db import db
from PIL import Image
from uuid import uuid4
import os
from PIL import UnidentifiedImageError


def validate(request_json: dict, schema: Schema) -> dict:
    if request_json is None:
        raise BadRequest('Os dados devem ser enviados via json')
    try:
        return schema.load(request_json)
    except ValidationError as validation_error:
        e = BadRequest(validation_error.messages)
        e.data = {
            'message': 'Erro de validação.',
            'errors': validation_error.messages
        }
        raise e


def save(instance: db.Model) -> db.Model:
    session = db.session()
    session.add(instance)
    session.commit()
    return instance


def delete(instance: db.Model) -> db.Model:
    print(dir(instance))
    session = db.session()
    session.delete(instance)
    session.commit()
    return instance


def save_image_as_jpeg(image_path, target_folder) -> str:
    """Converte imagem para jpeg e salva no diretório alvo com um nome novo e único

    :raises: :class:`UnidentifiedImageError`
    
    :returns: New file name
    """
    try:
        original_image = Image.open(image_path)
    except UnidentifiedImageError:
        raise BadRequest('Imagem inserida está corrompida ou não foi reconhecida. Extensões suportados: JPEG e PNG')
    except Image.DecompressionBombError:
        raise BadRequest(f'Imagem grande de mais. O número de pixels não pode ultrapassar {Image.MAX_IMAGE_PIXELS}')
    rgb_image = original_image.convert('RGB')
    new_filename = str(uuid4()) + '.jpeg'
    new_file_path = os.path.join(target_folder, new_filename)
    rgb_image.save(new_file_path, format='JPEG')
    return new_filename
