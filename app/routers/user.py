from fastapi import APIRouter , Response, status, HTTPException, Depends
from typing import List
from .. import models , schema, utils
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router=APIRouter()

@router.post("/users",response_model=schema.UserResponse)
async def create_user(user:schema.CreateUser, db:Session=Depends(get_db)):
    #hashing of password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    #save user into data base
    user_created= models.User(**user.dict())
    db.add(user_created)
    db.commit()
    db.refresh(user_created)

    return user_created

