from flask import Blueprint, request, jsonify
from core.db import db, User, ValidationError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, JWTManager


jwt = JWTManager()

blueprint = Blueprint('security_blueprint', __name__)

@blueprint.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Bad email or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


@blueprint.route("/register", methods=["POST"])
def register():
    email = request.json.get("email")
    password = request.json.get("password")

    try:
        new_user = User(email, password)
    except ValidationError as e:
        return jsonify({"error": e.messages}), 401

    session = db.session()
    session.add(new_user)
    session.commit()

    return jsonify(user={'email': new_user.email}), 201
