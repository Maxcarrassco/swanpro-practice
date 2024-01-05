#!/usr/bin/python3

from flask import Blueprint, abort, jsonify
from flask_pydantic import validate
from models import storage
from models.s_class import Class
from schemas.schemas import ClassSchema
from api.v1.auth.jwt_auth import auth

class_router = Blueprint("class_router",
                         __name__, url_prefix="/api/v1/classes")


@class_router.get("/")
@auth.login_required
def get_classes():
    try:
        classes = [v.to_dict() for _, v in storage.all(Class).items()]
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return classes


@class_router.post("/")
@auth.login_required(role="teacher")
@validate()
def create_classe(body: ClassSchema):
    classe = storage.get_object_by_label(Class, body.label)
    if classe:
        if classe.deleted:
            return jsonify(400, {"msg":"this class was deleted recently; unable to create this class again till after 3 months"})
        return jsonify(400, {"msg":"class already exists"})
    try:
        classe = Class(**(body.__dict__))
        storage.save()
    except Exception as e:
        print(e)
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return classe.to_dict()


@class_router.get("/<id>")
@auth.login_required
def get_classe(id: str):
    try:
        classe = storage.get_obj_by_id(Class, id)
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    if not classe or classe.deleted:
        return jsonify(404, {"msg": "Class not Found"})
    return classe.to_dict()


@class_router.put("/<id>")
@auth.login_required(role="teacher")
@validate()
def update_classe(id: str, body: ClassSchema):
    classe = storage.get_obj_by_id(Class, id)
    if not classe or classe.deleted:
        return jsonify(404, {"msg": "Class not Found"})
    classe.label = body.label
    try:
        storage.update(classe, id)
        storage.save()
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return "", 204


@class_router.delete("/<id>")
@auth.login_required(role="teacher")
def delete_classe(id: str):
    classe = storage.get_obj_by_id(Class, id)
    if not classe or classe.deleted:
        return jsonify(404, {"msg": "Class not Found"})
    try:
        storage.delete(classe)
        storage.save()
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return classe.to_dict()
