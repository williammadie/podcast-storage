from http import HTTPStatus
import os
import datetime
import jwt

from fastapi import APIRouter, HTTPException

import bcrypt
from pydantic import BaseModel

login_router = APIRouter()


def get_hashed_password(plain_text_password: str) -> str:
    return bcrypt.hashpw(plain_text_password.encode('utf8'), bcrypt.gensalt()).decode('utf8')


def check_password(plain_text_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_text_password.encode("utf8"), hashed_password.encode("utf8"))


def generate_access_token(data: dict, expires_in: int = 3600) -> str:
    expiration = datetime.datetime.now(
        datetime.timezone.utc) + datetime.timedelta(seconds=expires_in)
    payload = {**data, "exp": expiration}
    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
    return token


def verify_access_token(credentials):
    """
    Verifies the JWT token from the request headers.

    :param credentials: The HTTP bearer token credentials.
    :return: The decoded data if verification is successful.
    :raises: HTTPException if the token is invalid or expired.
    """
    token = credentials
    try:
        # Decode the token
        decoded_data = jwt.decode(token, os.getenv(
            "SECRET_KEY"), algorithms=["HS256"])
        return decoded_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserLogin(BaseModel):
    username: str
    password: str


@login_router.post("/")
async def admin_login(body: UserLogin):
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password_hash = os.getenv("ADMIN_PASSWORD_HASH")

    if admin_username is None or admin_password_hash is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail={"reason": "No admin defined"}
        )

    if body.username != admin_username:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={"reason": "Incorrect username or password"}
        )

    if not check_password(body.password, admin_password_hash):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={"reason": "Incorrect username or password"}
        )

    return generate_access_token({"admin_username": admin_username})
