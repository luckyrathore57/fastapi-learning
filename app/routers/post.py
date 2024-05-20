from fastapi import APIRouter , Response, status, HTTPException, Depends
from typing import List
from .. import models , schema, utils, oauth2
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=['post']
)

@router.get("/", response_model=List[schema.PostResponseVote])
async def get_all_post(db:Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:str=""):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts



@router.post("/",status_code=status.HTTP_404_NOT_FOUND, response_model=schema.PostResponse)
async def createPost(post : schema.CreatePost, db:Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    post_created= models.Post(owner_id=current_user.id ,**post.dict())
    db.add(post_created)
    db.commit()
    db.refresh(post_created)
    return post_created


@router.get("/{id}", response_model=schema.PostResponseVote)
async def get_post_with_id(id:int, response:Response,  db:Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):

    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id equal to {id} not found")
    
    return post


@router.delete("/{id}")
async def delete_post_with_id(id:int, db:Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):

    post_query=db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user is not allowed to perform this operation")
    post_query.delete(synchronize_session=False) #need_to_learn_about
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.PostResponse)
async def update_post_with_id(id:int,post_new:schema.CreatePost, db:Session=Depends(get_db),current_user: int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="user is not allowed to perform this operation")
    
    post_query.update(post_new.dict(),synchronize_session=False)
    db.commit()
    
    return post_query.first()

