from flask_restx import Api, fields, Resource

api = Api(title='Blog', description='Desafio Framework')


class Post(Resource): pass
class Comment(Resource): pass
class Album(Resource): pass
class Foto(Resource): pass