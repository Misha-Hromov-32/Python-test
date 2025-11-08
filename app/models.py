from typing import Optional

from pydantic import BaseModel


class Movietop(BaseModel):
    id: int
    name: str
    cost: int
    director: str
    watched: bool = False
    description: Optional[str] = None
    poster_path: Optional[str] = None


class User(BaseModel):
    username: str
    password: str

