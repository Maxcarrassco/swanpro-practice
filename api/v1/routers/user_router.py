#!/usr/bin/python3

from flask import Blueprint, abort, jsonify
from flask_pydantic import validate
from models import storage
from models.users import User
from models.subject import Subject
from schemas.schemas import CreateUserSchema
from schemas.schemas import UpdateUserSchema
from api.v1.auth.jwt_auth import auth
from utils.password_utils import hash_password

user_router = Blueprint("user_router", __name__, url_prefix="/api/v1/users")


@user_router.get("/")
@auth.login_required(role="teacher")
def get_users():
    try:
        users = [v.to_dict() for _, v in storage.all(User).items()]
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return users


@user_router.post("/")
@validate()
def create_user(body: CreateUserSchema):
    try:
        user = User(**(body.__dict__))
        user.gender = user.gender.value
        user.role = user.role.lower()
        user.password = hash_password(user.password)
        storage.save()
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return jsonify(201, {"msg": "user Successfully created!"})


@user_router.get("/<id>")
def get_user(id: str):
    try:
        user = storage.get_obj_by_id(User, id)
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    if not user:
        return jsonify(404, {"msg": "user not Found"})
    return user.to_dict()


@user_router.put("/<id>")
@auth.login_required()
@validate()
def update_user(id: str, body: UpdateUserSchema):
    user = storage.get_obj_by_id(User, id)
    if not user:
        return jsonify(404, {"msg": "user not Found"})
    user.gender = body.gender.value
    user.name = body.name
    user.age = body.age
    try:
        storage.update(user, id)
        storage.save()
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return "", 204


@user_router.delete("/<id>")
@auth.login_required()
def delete_user(id: str):
    current_user: User = auth.current_user()
    if current_user.id != id and current_user.role != "teacher":
        return abort(401, "Not authorized to view this resource")
    user = storage.get_obj_by_id(User, id)
    if not user:
        return jsonify(404, {"msg": "user not Found"})
    try:
        storage.delete(user)
        storage.save()
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return user.to_dict()
