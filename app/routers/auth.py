from fastapi import APIRouter, Depends, HTTPException

from ..data import movies_list
from ..database import get_user
from ..dependencies import get_current_user
from ..schemas.auth import LoginPayload, TokenResponse
from ..schemas.user import UserProfile, UserProfileResponse
from ..security import (
    create_access_token,
    get_access_log,
    get_access_token_ttl_seconds,
    hash_password,
    log_user_access,
)

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginPayload) -> TokenResponse:
    user = get_user(payload.username)
    if not user or user["password"] != hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    access_token = create_access_token(username=payload.username)
    return TokenResponse(
        access_token=access_token,
        expires_in=get_access_token_ttl_seconds(),
    )


@router.get("/user", response_model=UserProfileResponse)
async def get_user_profile(current_user: dict = Depends(get_current_user)) -> UserProfileResponse:
    username = current_user["username"]
    log_user_access(username)

    access_log = [timestamp.isoformat() + "Z" for timestamp in get_access_log(username)]
    profile = UserProfile(
        username=username,
        created_at=str(current_user["created_at"]),
    )

    return UserProfileResponse(
        profile=profile,
        access_log=access_log,
        movies=movies_list,
    )

