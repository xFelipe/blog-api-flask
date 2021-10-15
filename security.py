from flask import Blueprint, request, jsonify
from db import db, User, ValidationError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, JWTManager


jwt = JWTManager()

blueprint = Blueprint('security_blueprint', __name__)

@blueprint.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


@blueprint.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    try:
        new_user = User(username, password)
    except ValidationError as e:
        return jsonify({"error": e.messages}), 401

    session = db.session()
    session.add(new_user)
    session.commit()

    return jsonify(user={'username': new_user.username}), 201
