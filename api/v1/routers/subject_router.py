#!/usr/bin/python3

from flask import Blueprint, jsonify, abort
from flask_pydantic import validate
from models import storage
from models.subject import Subject
from models.s_class import Class
from schemas.schemas import SubjectSchema, SubjectUpdateSchema
from api.v1.auth.jwt_auth import auth
subject_router = Blueprint("subject_router",
                           __name__, url_prefix="/api/v1/subjects")


@subject_router.get("/")
@auth.login_required
def get_sujects():
    try:
        sujects = [v.to_dict() for _, v in storage.all(Subject).items()]
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return sujects


@subject_router.post("/")
@auth.login_required(role="teacher")
@validate()
def create_subject(body: SubjectSchema):
    sub_class = storage.get_object_by_label(Class, body.class_name)
    if not sub_class or sub_class.deleted:
        return abort(404, "class not found")
    subject = sub_class.get_subject_by_label(body.label)
    if subject:
        if subject.deleted:
            return jsonify(400, {"msg":"this subject was deleted recently; unable to create this subject again till after 3 months"})
        return jsonify(400, {"msg":"subject already exists"})
    try:
        sub_class.add_subject(body.label)
        storage.save()
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return jsonify(201, {"msg": "Subject Successfully created!"})


@subject_router.get("/<id>")
@auth.login_required
def get_subject(id: str):
    try:
        subject = storage.get_obj_by_id(Subject, id)
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    if not subject or subject.deleted:
        return jsonify(404, {"msg": "Subject not Found"})
    return subject.to_dict()


@subject_router.put("/<id>")
@auth.login_required(role="teacher")
@validate()
def update_subject(id: str, body: SubjectUpdateSchema):
    subject_db = storage.get_obj_by_id(Subject, id)
    if not subject_db or subject_db.deleted:
        return jsonify(404, {"msg": "Subject not Found"})
    subject_db.label = body.label
    try:
        storage.update(subject_db, id)
        storage.save()
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return "", 204


@subject_router.delete("/<id>")
@auth.login_required(role="teacher")
def delete_subject(id: str):
    subject = storage.get_obj_by_id(Subject, id)
    if not subject or subject.deleted:
        return jsonify(404, {"msg": "Subject not Found"})
    try:
        storage.delete(subject)
        storage.save()
    except Exception as e:
        print(e)
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return subject.to_dict()
