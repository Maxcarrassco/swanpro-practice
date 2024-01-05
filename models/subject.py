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
    

    def add_grade(self, grade: str) -> None:
        from models.grade import Grade
        """Add new grade for a student"""
        grade = Grade(subject_id=self.id, grade=grade)
        self.grades.append(grade)

    def delete_grade(self) -> None:
        from models.grade import Grade
        from models import storage
        """Delete a grade for a student"""
        grade = storage.get_obj_by_id(Grade, self.id)
        if not grade:
            return
        self.grades.remove(grade)
        storage.delete(grade)

    def compute_avg_grade(self) -> float:
        """Compute the average of a student for a specific subject"""
        count = 0
        curr_sum = 0
        for grade in self.grades:
            if grade.subject_id == self.id and not self.deleted:
                curr_sum += grade.grade
                count += 1
        return curr_sum / count if count > 0 else 0

