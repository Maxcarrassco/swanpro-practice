#!/usr/bin/python3

from typing import List
from sqlalchemy import String
from models import base_model
from models.class_subject import association_table
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Class(base_model.BaseModel):
    from models.users import User
    from models.subject import Subject
    __tablename__ = "class"
    label: Mapped[str] = mapped_column(String(250))
    students: Mapped[List["User"]] = relationship(back_populates="classes")
    subjects: Mapped[List[Subject]] = relationship(secondary=association_table)
