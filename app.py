from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app, title='')

@app.route('/hello')
def hello():
    return {'message': 'Hello world!'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
