from flask import Blueprint, request, jsonify
from db import User
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, JWTManager


jwt = JWTManager()

blueprint = Blueprint('security_blueprint', __name__)

@blueprint.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    user = User.query.filter_by(username=username).first()
    if not user or not safe_str_cmp(user.password, password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)
