#!/usr/bin/python3

from typing import List, Union, Dict, Any
from sqlalchemy import String
from models import base_model
from models.subject import Subject
from models.class_subject import association_table
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Class(base_model.BaseModel):
    from models.users import User
    __tablename__ = "classes"
    label: Mapped[str] = mapped_column(String(250))
    students: Mapped[List["User"]] = relationship(back_populates="classes")
    subjects: Mapped[List[Subject]] = relationship(secondary=association_table)


    def get_subject_by_label(self, label: str) -> Union[Subject, None]:

        for subject in self.subjects:
            if label == subject.label:
                return subject
        return None

    def add_subject(self, label: str) -> None:
        from models import storage
        subject = Subject(label=label)
        self.subjects.append(subject)
   

    def add_student(self, student) -> None:
        from models import storage
        self.students.append(student)
