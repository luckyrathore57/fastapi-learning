from fastapi import APIRouter , Response, status, HTTPException, Depends
from typing import List
from .. import models , schema, utils
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/users",
    tags=['user']
)

@router.post("/",response_model=schema.UserResponse)
def create_user(user:schema.UserCreated, db:Session=Depends(get_db)):
    #check whether user already exist in database
    user_from_database=db.query(models.User).filter(models.User.email==user.email).first()
    if user_from_database:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user already exist with this email")

    #hashing of password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    #save user into data base
    user_created= models.User(**user.dict())
    
    db.add(user_created)
    db.commit()
    db.refresh(user_created)

    return user_created

