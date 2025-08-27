from typing import List
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    sub: str
    username: str
    is_premium: bool = False
    email: str = ""
    groups: List[str] = []
