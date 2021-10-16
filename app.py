from flask import Flask
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from core.security import jwt, blueprint as security_bp
from core.db import db
from api_v1 import blueprint as api_v1_bp, api as api_v1


basedir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C_H-l786ithiul76u5yrht77rth'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'sqlite.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(security_bp, url_prefix='/api')
app.register_blueprint(api_v1_bp, url_prefix='/api/v1')


@app.route('/hello')
@jwt_required()
def hello():
    current_user_id = get_jwt_identity()
    return {'message': 'Hello world!', 'user': current_user_id}


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db
    }


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
