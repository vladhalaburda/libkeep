from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: str

    class Config:
        orm_mode = True

class UserInDB(UserBase):
    hashed_password: str