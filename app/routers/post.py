from fastapi import APIRouter , Response, status, HTTPException, Depends
from typing import List
from .. import models , schema, utils
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router=APIRouter()

@router.get("/posts", response_model=List[schema.PostResponse])
async def get_all_post(db:Session=Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts """)
    # posts=cursor.fetchall()

    posts = db.query(models.Post).all()

    return {"status":"done done" , "data":posts}



@router.post("/posts",status_code=status.HTTP_404_NOT_FOUND, response_model=schema.PostResponse)
async def createPost(post : schema.CreatePost, db:Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title,post.content,post.published))
    # post_created=cursor.fetchone()
    # conn.commit()

    post_created= models.Post(**post.dict())
    db.add(post_created)
    db.commit()
    db.refresh(post_created)
    return post_created


@router.get("/posts/{id}", response_model=schema.PostResponse)
async def get_post_with_id(id:int, response:Response,  db:Session=Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post=cursor.fetchone()

    post=db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f"post with id equal to {id} not found"}
        #
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id equal to {id} not found")
    

    
    return post


@router.delete("/posts/{id}")
async def delete_post_with_id(id:int, db:Session=Depends(get_db)):

    post=db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    
    post.delete(synchronize_session=False) #need_to_learn_about
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schema.PostResponse)
async def update_post_with_id(id:int,post:schema.CreatePost, db:Session=Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    
    return post_query.first()

