from pydantic import BaseModel
from typing import Optional

class Movietop(BaseModel):
    name: str
    id: int
    cost: int
    director: str
    watched: bool = False
    description: Optional[str] = None
    poster_path: Optional[str] = None