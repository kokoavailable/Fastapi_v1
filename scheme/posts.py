from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    board_sn: int

class PostOut(PostBase):
    post_sn: int
    board_sn: int
    user_sn: int
