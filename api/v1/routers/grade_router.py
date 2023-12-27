#!/usr/bin/python3

from flask import Blueprint, abort, jsonify
from flask_pydantic import validate
from models import storage
from models.users import User
from models.subject import Subject
from schemas.schemas import GradeSchema
from schemas.schemas import RecordGradeSchema
from api.v1.auth.jwt_auth import auth

grade_router = Blueprint("grade_router", __name__, url_prefix="/api/v1/grades")


@grade_router.get("/")
@auth.login_required()
def get_grades():
    current_user: User = auth.current_user()
    if current_user.id != id and current_user.role != "teacher":
        return abort(401, "Not authorized to view this resource")
    user = storage.get_obj_by_id(User, current_user.id)
    if not user:
        return jsonify(404, {"msg": "user not Found"})
    return [v.to_dict() for v in user.grades]


@grade_router.post("/")
@auth.login_required(role="teacher")
@validate()
def record_grade(body: RecordGradeSchema):
    user = storage.get_obj_by_id(User, body.user_id)
    if not user:
        return jsonify(404, {"msg": "user not Found"})
    if user.role != "student":
        return jsonify(400, {"msg": "Can't assigned grade to teacher"})
    subject = storage.get_obj_by_id(Subject, body.subject_id)
    if not subject:
        return jsonify(404, {"msg": "Subject not Found"})
    try:
        user.add_grade(body.subject_id, body.grade)
        storage.save()
    except Exception as err:
        print(err)
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return jsonify(201, {"msg": "Grade recorded Successfully!"})


@grade_router.post("/avgs")
@auth.login_required
@validate()
def get_all_sub_avg_grade(body: GradeSchema):
    current_user: User = auth.current_user()
    if current_user.id != id and current_user.role != "teacher":
        return abort(401, "Not authorized to view this resource")
    user = storage.get_obj_by_id(User, body.user_id)
    if not user:
        return jsonify(404, {"msg": "user not Found"})
    if user.role != "student":
        return jsonify(400, {"msg": "Teacher don't have grades! Unable to calculate average"})
    obj = {}
    storage.get_user_avg_grade(user.id)
    for grade in user.grades:
        subject = storage.get_obj_by_id(Subject, grade.subject_id)
        key = f"{subject.label}.{subject.id}"
        if key in obj:
            obj[key].append(grade.grade)
        else:
            obj[key] = [grade.grade]
    averages = {}
    for key, grade in obj.items():
        name, k = key.split(".")
        avg = sum(grade) / len(grade)
        averages[key] = {"subject": name, "subject_id": k, "avg": avg}
    return averages


@grade_router.post("/avg")
@auth.login_required
@validate()
def avg_grade(body: GradeSchema):
    current_user: User = auth.current_user()
    if current_user.id != id and current_user.role != "teacher":
        return abort(401, "Not authorized to view this resource")
    user = storage.get_obj_by_id(User, body.user_id)
    if not user:
        return jsonify(404, {"msg": "user not Found"})
    if user.role != "student":
        return jsonify(400, {"msg": "Teacher don't have grades! Unable to calculate average"})
    subject = storage.get_obj_by_id(Subject, body.subject_id)
    if not subject:
        return jsonify(404, {"msg": "Subject not Found"})
    avg = user.compute_avg_grade(body.subject_id)
    if int(avg) <= 0:
        return jsonify(400, {"msg": "You have not taken any exam!"})
    return {"avg": avg, "subject": subject.label}
