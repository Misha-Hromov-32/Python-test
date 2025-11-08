from fastapi import Depends, Header, HTTPException

from .database import get_user
from .security import decode_access_token


def extract_bearer_token(authorization: str = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing.")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid authorization header.")
    return token


def get_current_user(token: str = Depends(extract_bearer_token)):
    username = decode_access_token(token)
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user

