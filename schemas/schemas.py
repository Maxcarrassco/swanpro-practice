from pydantic import BaseModel, EmailStr
from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class CreateUserSchema(BaseModel):
    name: str
    age: int
    role: str
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


class ClassSchema(BaseModel):
    label: str


class SubjectSchema(BaseModel):
    label: str


class RecordGradeSchema(BaseModel):
    user_id: str
    grade: int
    subject_id: str


class GradeSchema(BaseModel):
    user_id: str
    subject_id: str
