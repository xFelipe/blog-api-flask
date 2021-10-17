from marshmallow import Schema, ValidationError
from werkzeug.exceptions import BadRequest
from core.db import db


def validate(request_json: dict, schema: Schema) -> dict:
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