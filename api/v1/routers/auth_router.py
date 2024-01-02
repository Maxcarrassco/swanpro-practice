from flask import Blueprint, abort
from flask_pydantic import validate
from schemas.schemas import LoginSchema, LogoutSchema
from utils.password_utils import verify_password
from models import storage
from models.blocklisted_token import BlockListedToken
from api.v1.auth.jwt_auth import create_access_token, auth, decode_access_token

auth_router = Blueprint("auth_router", __name__, url_prefix="/api/v1/auth")


@auth_router.post('/login')
@validate()
def login(body: LoginSchema):
    """Return user access token."""
    user = storage.get_user_by_email(body.email)
    if not user:
        return abort(401, "Invalid email or password")

    if not verify_password(body.password, user.password):
        return abort(401, "Invalid email or password")

    data = {
            'id': user.id,
            'email': user.email,
            'role': user.role
            }
    token = create_access_token(data)
    return {
            'access_token': token,
            'token_type': 'bearer'
            }


@auth.login_required()
@auth_router.post('/logout')
@validate()
def logout(body: LogoutSchema):
    """Block List a access token"""
    decode_access_token(body.token)
    if storage.get_blocklisted_token_by_token(body.token):
        return {"msg": "unable to logout this user"}, 400
    token = BlockListedToken(**(body.__dict__))
    storage.save()
    return {"msg": "Logout Successful"}
    
