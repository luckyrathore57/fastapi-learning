from fastapi import APIRouter , Response, status, HTTPException, Depends
from ..oauth2 import get_current_user
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schema



router=APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/{id}")
def vote_function(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="wrong request send")
    
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==id , models.Vote.user_id==current_user.id)
    if not vote_query.first():
        vote=models.Vote(post_id=id,user_id=current_user.id)
        db.add(vote)
        db.commit()
        db.refresh(vote)
        return {"message":"like post succesfully"}
    else:
        vote=vote_query.first()
        vote_query.delete()
        db.commit()
        return {"message":"unlike post succesfully"}
