from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List
import hashlib

import jwt
from fastapi import HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError

from .core.config import get_settings

settings = get_settings()
_access_log: Dict[str, List[datetime]] = defaultdict(list)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_access_token(username: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.utcnow() + expires_delta
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except ExpiredSignatureError as exc:
        raise HTTPException(status_code=401, detail="Token has expired.") from exc
    except InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Invalid token.") from exc

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload.")
    return username


def log_user_access(username: str) -> None:
    _access_log[username].append(datetime.utcnow())


def get_access_log(username: str) -> List[datetime]:
    return list(_access_log.get(username, []))


def get_access_token_ttl_seconds() -> int:
    return settings.access_token_expire_minutes * 60

