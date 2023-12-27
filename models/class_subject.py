#!/usr/bin/python3

from sqlalchemy import Column, ForeignKey, Table
from models.base_model import BaseModel

association_table = Table(
    "class_subject",
    BaseModel.metadata,
    Column("class_id", ForeignKey("class.id"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
)
