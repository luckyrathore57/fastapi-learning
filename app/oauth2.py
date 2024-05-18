from jose import JWTError,jwt
from datetime import datetime, timedelta
from fastapi import Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import schema,database,models


SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

oauth2_schema=OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data=schema.TokenData(id=id)
    except JWTError:
        raise credential_exception
    
    return token_data



def get_current_user(token:str = Depends(oauth2_schema)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credential" , headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token,credential_exception)



