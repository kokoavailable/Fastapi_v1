from pydantic import BaseModel

# 계정 api
class UserBase(BaseModel):
    fullname: str
    email: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str

class UserOut(UserBase):
    user_sn: int
