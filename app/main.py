from fastapi import FastAPI , Response, status, HTTPException, Depends
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional, List
from . import models , schema, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import user, post, auth,vote

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




@app.get("/")
async def root():
    return {"message":"hello world"}








