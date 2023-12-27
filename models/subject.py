#!/usr/bin/python3

from typing import List
from sqlalchemy import String
from models import base_model
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Subject(base_model.BaseModel):

    from models.grade import Grade
    __tablename__ = "subjects"
    label: Mapped[str] = mapped_column(String(250))
    grades: Mapped[List[Grade]] = relationship()
