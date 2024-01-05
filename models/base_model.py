#!/usr/bin/python3

from typing import Any
from sqlalchemy import func, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from uuid import uuid4


class BaseModel(DeclarativeBase):
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())

    def __init__(self, **kwargs: Any):
        if kwargs:
            for key, val in kwargs.items():
                setattr(self, key, val)
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
            if "id" not in kwargs:
                self.id = str(uuid4())
        else:
            self.created_at = datetime.utcnow()
            self.updated_at = None
            self.id = str(uuid4())
        from models import storage
        storage.new(self)

    def __str__(self) -> str:
        return f"({self.__class__.__name__}) {self.to_dict()}"

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}) {self.to_dict()}"

    def to_dict(self):
        data = self.__dict__.copy()
        del data["_sa_instance_state"]
        del data["deleted"]
        if data.get("created_at") and isinstance(data.get("created_at"), datetime):
            data["created_at"] = data["created_at"].isoformat()
        if data.get("updated_at") and isinstance(data.get("updated_at"), datetime):
            data["updated_at"] = data["updated_at"].isoformat()
        return data
