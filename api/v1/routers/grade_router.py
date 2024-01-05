#!/usr/bin/python3

from flask import Blueprint, abort, jsonify, request
from flask_pydantic import validate
from models import storage
from models.users import User
from models.subject import Subject
from models.grade import Grade
from models.s_class import Class
from schemas.schemas import GradeSchema
from schemas.schemas import RecordGradeSchema
from api.v1.auth.jwt_auth import auth
from utils.password_utils import hash_password
import openpyxl
import os

grade_router = Blueprint("grade_router", __name__, url_prefix="/api/v1/grades")


@grade_router.get("/")
@auth.login_required(role="teacher")
def get_all_grades():
    try:
        grades = [v.to_dict() for _, v in storage.all(Grade).items()]
    except Exception:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return grades


@grade_router.post("/students/grades")
@auth.login_required()
@validate()
def get_grades(body: GradeSchema):
    current_user: User = auth.current_user()
    if current_user.id != body.user_id and current_user.role != "teacher":
        return abort(401, "Not authorized to view this resource")
    user = storage.get_obj_by_id(User, body.user_id)
    if user.role == "teacher":
        return abort(400, "expected student got teacher")
    if not user:
        return jsonify(404, {"msg": "user not Found"})
    if not user.classes:
        return []
    subject = user.classes.get_subject_by_label(body.subject)
    if not subject:
        return []
    return [v.to_dict() for v in subject.grades]


@grade_router.post("/upload")
@auth.login_required(role="teacher")
def upload_grade():
    if "file" not in request.files:
        return jsonify(400, {"msg":"invalid request"})
    file = request.files["file"]
    if file.filename == "":
        return jsonify(400, {"msg":"invalid request"})

    try:
        wb = openpyxl.load_workbook(file)
        ws = wb.active 

        data = ws.iter_rows(values_only=True)
        field = str(data.__next__()[0]).replace(")", "").split("(")
        if len(field) != 2:
            return jsonify(400, {"msg":"invalid document format"})
        subject_name = field[0]
        class_name = field[1]
    except Exception:
        return jsonify(400, {"msg":"invalid document format"})

    try:
        s_class = storage.get_object_by_label(Class, class_name)
        if not s_class:
            s_class = Class(label=class_name)
            storage.save()
        subject = storage.get_object_by_label(Subject, subject_name)
        if not subject:
            subject = Subject(label=subject_name)
        s_class.subjects.append(subject)
        storage.save()
    except Exception as e:
        print(e)
        return abort(500, "Oops! Something went wrong! We are working on it!")

    students = []

    for row in data:
        if row[0] == None or str(row[0]).strip() == "Name":
            continue
        if len(row) != 5:
            return abort(400, "invalid document format")
        student = {}
        student["name"] = row[0]
        student["email"] = row[1]
        student["gender"] = row[2]
        student["age"] = row[3]
        student["grade"] = row[4]
        student["class_id"] = s_class.id
        student["role"] = "student"
        student["password"] = hash_password(os.environ["STUDENT_DEFAULT_PASSWORD"])
        students.append(student)

    for student in students:
        grade = student["grade"]
        del student["grade"]
        stud = storage.get_user_by_email(student["email"])
        if not stud:
            stud = User(**student)
        subject.add_grade(grade)
        s_class.add_student(stud)
        storage.save()

    return {"msg": "Grade uploaded successfully"}


@grade_router.post("/")
@auth.login_required(role="teacher")
@validate()
def record_grade(body: RecordGradeSchema):
    user = storage.get_obj_by_id(User, body.user_id)
    if not user:
        return jsonify(404, {"msg": "user not Found"})
    if user.role != "student":
        return jsonify(400, {"msg": "Can't assigned grade to teacher"})
    if not user.classes:
        return jsonify(400, {"msg": "student is not doing this subject"})
    subject = user.classes.get_subject_by_label(body.subject)
    if not subject:
        return jsonify(400, {"msg": "student is not doing this subject"})
    try:
        subject.add_grade(body.grade)
        storage.save()
    except Exception as err:
        return abort(500, "Oops! Something went wrong! We are working on it!")
    return jsonify(201, {"msg": "Grade recorded Successfully!"})


@grade_router.get("/avgs/<user_id>")
@auth.login_required
def get_all_sub_avg_grade(user_id: str):
    current_user: User = auth.current_user()
    if current_user.id != user_id and current_user.role != "teacher":
        return abort(401, "Not authorized to view this resource")
    user = storage.get_obj_by_id(User, user_id)
    if not user:
        return jsonify(404, {"msg": "user not Found"})
    if user.role != "student":
        return jsonify(400, {"msg": "Teacher don't have grades! Unable to calculate average"})
    obj = {}
    for subject in user.classes.subjects:
        if subject.deleted:
            continue
        for grade in subject.grades:
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
    if current_user.id != body.user_id and current_user.role != "teacher":
        return abort(401, "Not authorized to view this resource")
    user = storage.get_obj_by_id(User, body.user_id)
    if not user:
        return jsonify(404, {"msg": "user not Found"})
    if user.role != "student":
        return jsonify(400, {"msg": "Teacher don't have grades! Unable to calculate average"})
    if not user.classes:
        return jsonify(400, {"msg": "You have not taken any exam in this subject!"})
    subject = user.classes.get_subject_by_label(body.subject)
    if not subject:
        return jsonify(404, {"msg": "Subject not Found"})
    avg = subject.compute_avg_grade()
    if int(avg) <= 0:
        return jsonify(400, {"msg": "You have not taken any exam in this subject!"})
    return {"avg": avg, "subject": subject.label}
