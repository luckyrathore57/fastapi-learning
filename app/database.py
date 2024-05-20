from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings



# import psycopg2
# from psycopg2.extras import RealDictCursor 
# import time
# while True:
#     try:
#         conn=psycopg2.connect(user='postgres', password='572002', host='localhost', database='fastapi', cursor_factory=RealDictCursor)
#         cursor=conn.cursor() 
#         print("connection done succesfully")
#         break

#     except Exception as error:
#         print(error)
#         time.sleep(3)


        

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
