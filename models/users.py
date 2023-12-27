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
    class_id: Mapped[Optional[int]] = mapped_column(ForeignKey("class.id"))
    classes: Mapped[Optional["Class"]] = relationship(
        back_populates="students")
    grades: Mapped[List[Grade]] = relationship()

    def add_grade(self, subject_id: str, grade: str) -> None:
        from models.grade import Grade
        """Add new grade for a student"""
        grade = Grade(subject_id=subject_id, grade=grade, user_id=self.id)
        self.grades.append(grade)

    def delete_grade(self, subject_id: str) -> None:
        from models.grade import Grade
        from models import storage
        """Delete a grade for a student"""
        grade = storage.get_obj_by_id(Grade, subject_id)
        if not grade or grade.student_id != self.id:
            return
        self.grades.remove(grade)
        storage.delete(grade)

    def compute_avg_grade(self, subject_id: str) -> float:
        """Compute the average of a student for a specific subject"""
        count = 0
        curr_sum = 0
        for grade in self.grades:
            if grade.subject_id == subject_id:
                curr_sum += grade.grade
                count += 1
        return curr_sum / count

    def to_dict(self):
        user = super().to_dict()
        del user["password"]
        return user
