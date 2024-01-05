from pydantic import BaseModel, EmailStr
from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Role(Enum):
    TEACHER = "teacher"
    STUDENT = "student"


class CreateUserSchema(BaseModel):
    name: str
    age: int
    role: Role
    gender: Gender
    password: str
    email: EmailStr


class UpdateUserSchema(BaseModel):
    name: str
    age: int
    gender: Gender


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class LogoutSchema(BaseModel):
    token: str


class ClassSchema(BaseModel):
    label: str


class SubjectSchema(BaseModel):
    class_name: str
    label: str

class SubjectUpdateSchema(BaseModel):
    label: str


class RecordGradeSchema(BaseModel):
    user_id: str
    grade: int
    subject: str


class GradeSchema(BaseModel):
    user_id: str
    subject: str
