from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title:str
    content:str
    published: bool=True


class CreatePost(PostBase):
    pass


class PostResponse(PostBase):
    id:int
    created_at:datetime
    class Config:               #need_to_learn_about #pydantic model and sqlalchemy model
        orm_mode = True


class CreateUser(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode = True