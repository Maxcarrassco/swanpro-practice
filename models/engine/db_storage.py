#!/usr/bin/python3

from datetime import datetime
import os
from typing import Union
from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker
from models.users import User
from models.subject import Subject
from models.s_class import Class
from models.grade import Grade
from models.base_model import BaseModel

load_dotenv()

DBURL = os.environ["DB_URL"]


class DBStorage:
    __session = None
    __engine = None

    def __init__(self) -> None:
        self.__engine = create_engine(DBURL, pool_pre_ping=True)

    def new(self, ob: BaseModel):
        """Add new objects to the current db session"""
        if not self.__session:
            return
        self.__session.add(ob)

    def reload(self):
        """Init the db"""
        if not self.__engine:
            return
        BaseModel.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def save(self):
        """Commit the current session to db"""
        if not self.__session:
            return
        self.__session.commit()

    def all(self, ob: Union[BaseModel, None] = None,
            offset: int = 0, limit: int = 40):
        """Get the specific list of objects or all types of object from db"""
        objs = {}
        if not self.__session:
            return objs
        if not ob:
            for model in [Class, User, Subject]:
                result = self.__session.query(model).offset(
                    offset).limit(limit).all()
                for obj in result:
                    key = f"{type(obj).__name__}.{obj.id}"
                    objs[key] = obj
            return objs
        result = self.__session.query(ob).offset(offset).limit(limit).all()
        for obj in result:
            key = f"{type(obj).__name__}.{obj.id}"
            objs[key] = obj
        return objs

    def get_obj_by_id(self, ob: BaseModel, id: str) -> Union[BaseModel, None]:
        if not self.__session:
            return None
        result = self.__session.query(ob).where(ob.id == id).first()
        return result

    def get_user_by_email(self, email: str) -> Union[User, None]:
        """Get a user by email: return None if the user is not found"""
        if not self.__session:
            return None
        result = self.__session.query(User).where(User.email == email).first()
        return result

    def get_user_avg_grade(self, user_id: str):
        if not self.__session:
            return None
        avg_grade = self.__session.query(
            func.avg(Grade.grade).label('average')).filter(
            Grade.user_id == user_id).group_by(Grade.subject_id).all()
        return avg_grade

    def close_session(self):
        """Close the current session"""
        if not self.__session:
            return
        self.__session.close()

    def delete(self, ob: BaseModel) -> None:
        """Delete the object passed from db session"""
        if not self.__session:
            return
        self.__session.delete(ob)

    def update(self, ob: BaseModel, id: int) -> None:
        """Update the object passed in db session"""
        if not self.__session:
            return
        cls = type(ob)
        ob.updated_at = datetime.utcnow()
        self.__session.query(cls).where(cls.id == id).update(ob.to_dict())
