from pydantic import BaseModel
from typing import Optional

class BoardBase(BaseModel):
    name: str
    public: bool

class BoardCreate(BoardBase):
    pass

class BoardOut(BoardBase):
    board_sn: int
    user_sn: int

class BoardOutWithPostCount(BoardOut):
    post_count: int

class BoardUpdate(BaseModel):
    name: Optional[str] = None
    public: Optional[bool] = None