#!/usr/bin/python3

from sqlalchemy import ForeignKey
from models import base_model
from sqlalchemy.orm import Mapped, mapped_column


class Grade(base_model.BaseModel):
    __tablename__ = "grades"
    grade: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
