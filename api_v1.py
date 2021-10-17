from flask import Blueprint
from flask_restx import Api, Resource
from apis.post import ns as post_ns


blueprint = Blueprint('api_v1', __name__)
api = Api(blueprint, title='Blog', description='Desafio Framework')
api.add_namespace(post_ns)


class Comment(Resource): pass
class Album(Resource): pass
class Foto(Resource): pass
