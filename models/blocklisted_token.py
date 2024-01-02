#!/usr/bin/python3

from typing import List
from sqlalchemy import String
from models import base_model
from models.class_subject import association_table
from sqlalchemy.orm import Mapped, mapped_column, relationship


class BlockListedToken(base_model.BaseModel):
    __tablename__ = "blocklisted_tokens"
    token: Mapped[str] = mapped_column(String(250))
