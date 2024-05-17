from fastapi import FastAPI , Response, status, HTTPException, Depends
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from . import models , schema
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

models.Base.metadata.create_all(bind=engine)

app=FastAPI()


pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
while True:
    try:
        conn=psycopg2.connect(user='postgres', password='572002', host='localhost', database='fastapi', cursor_factory=RealDictCursor)
        cursor=conn.cursor() 
        print("connection done succesfully")
        break

    except Exception as error:
        print(error)
        time.sleep(3)


        



# def find_post_by_id(id:int)->schema.CreatePost|None:
#     for post in dummy_post:
#         if post['id']==id:
#             return post
        

# def find_index_by_id(id:int)->int|None:
#     for i,post in enumerate(dummy_post):
#         if post['id']==id:
#             return i


@app.get("/")
async def root():
    return {"message":"hello world"}

@app.get("/posts", response_model=List[schema.PostResponse])
async def get_all_post(db:Session=Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts """)
    # posts=cursor.fetchall()

    posts = db.query(models.Post).all()

    return {"status":"done done" , "data":posts}



@app.post("/posts",status_code=status.HTTP_404_NOT_FOUND, response_model=schema.PostResponse)
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


@app.get("/posts/{id}", response_model=schema.PostResponse)
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


@app.delete("/posts/{id}")
async def delete_post_with_id(id:int, db:Session=Depends(get_db)):

    post=db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    
    post.delete(synchronize_session=False) #need_to_learn_about
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schema.PostResponse)
async def update_post_with_id(id:int,post:schema.CreatePost, db:Session=Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} not found")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    
    return post_query.first()


@app.post("/users",response_model=schema.UserResponse)
async def create_user(user:schema.CreateUser, db:Session=Depends(get_db)):
    user_created= models.User(**user.dict())
    db.add(user_created)
    db.commit()
    db.refresh(user_created)
    return user_created


