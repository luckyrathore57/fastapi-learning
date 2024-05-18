from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schema,models,database,utils,oauth2


router=APIRouter(
    tags=['Authentication']
)

@router.post('/login',response_model=schema.Token)
def login_function(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    
    user=db.query(models.User).filter( user_credentials.username == models.User.email ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid email adress")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="wrong password")
    
    #create token & return token

    access_token = oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token":access_token,"token_type":"bearer"}