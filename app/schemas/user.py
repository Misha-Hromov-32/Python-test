from typing import List

from pydantic import BaseModel

from ..models import Movietop


class UserProfile(BaseModel):
    username: str
    created_at: str


class UserProfileResponse(BaseModel):
    profile: UserProfile
    access_log: List[str]
    movies: List[Movietop]

