from fastapi import FastAPI , Response, status, HTTPException, Depends
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from . import models , schema, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import user, post, auth

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

while True:
    try:
        conn=psycopg2.connect(user='postgres', password='572002', host='localhost', database='fastapi', cursor_factory=RealDictCursor)
        cursor=conn.cursor() 
        print("connection done succesfully")
        break

    except Exception as error:
        print(error)
        time.sleep(3)


        

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message":"hello world"}








