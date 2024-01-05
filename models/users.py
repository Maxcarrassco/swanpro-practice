#!/usr/bin/python3

from typing import List, Optional
from sqlalchemy import ForeignKey, String
from models import base_model
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(base_model.BaseModel):
    from models.grade import Grade
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(String(250))
    email: Mapped[str] = mapped_column(String(250), unique=True)
    password: Mapped[str] = mapped_column(String(250))
    role: Mapped[str] = mapped_column(String(80))
    gender: Mapped[str] = mapped_column(String(80))
    age: Mapped[int] = mapped_column()
    class_id: Mapped[Optional[int]] = mapped_column(ForeignKey("classes.id"))
    classes: Mapped[Optional["Class"]] = relationship(
        back_populates="students")

    def to_dict(self):
        user = super().to_dict()
        del user["password"]
        return user
