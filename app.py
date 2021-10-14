from flask import Flask, request, jsonify
from flask_restx import Api, fields, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import safe_str_cmp
import os
from db import db, User
from security import jwt, blueprint as security_bp


basedir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C_H-l786ithiul76u5yrht77rth'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'sqlite.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(security_bp, url_prefix='/api')

api = Api(app, title='Blog', description='Desafio Framework')


class Post(Resource): pass
class Comment(Resource): pass
class Album(Resource): pass
class Foto(Resource): pass


@app.route('/hello')
@jwt_required()
def hello():
    current_user_id = get_jwt_identity()
    return {'message': 'Hello world!', 'user': current_user_id}


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
