from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreated(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    username:EmailStr
    password:str



class PostBase(BaseModel):
    title:str
    content:str
    published: bool=True


class CreatePost(PostBase):
    pass


class PostResponse(PostBase):
    id:int
    created_at:datetime
    owner:UserResponse
    
    class Config:               #need_to_learn_about #pydantic model and sqlalchemy model
        orm_mode = True



class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None