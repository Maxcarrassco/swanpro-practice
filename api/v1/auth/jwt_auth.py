#!/usr/bin/python3
"""Handle JWT"""
from jose import jwt, JWTError
from functools import wraps
from typing import Dict
from flask import abort, request
from datetime import datetime, timedelta
from models import storage
from models.users import User
from flask_httpauth import HTTPTokenAuth
import os


auth = HTTPTokenAuth(scheme='Bearer')


def create_access_token(data: Dict) -> str:
    """Generate Access Token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(os.environ['JWT_TIME_TO_LIVE']))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, os.environ['JWT_SECRET'])


def decode_access_token(token: str) -> Dict:
    """Decode user access token."""
    try:
        user_data = jwt.decode(
                token, os.environ['JWT_SECRET'], algorithms=os.environ['JWT_ALGORITHM'])
        return user_data
    except JWTError:
        return abort(401, 'Could not validate credentials')


@auth.verify_token
def verify_token(token):
    """Return login user."""
    data = decode_access_token(token)
    user = storage.get_obj_by_id(User, data["id"])
    if not user:
        return abort(401, 'Could not validate credentials')
    return user


@auth.get_user_roles
def user_get_roles(user):
    return user.role
