from passlib.context import CryptContext


pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(strInput:str)->str:
    return pwd_context.hash(strInput)

def verify(str1,str_hashed)->bool:
    return pwd_context.verify(str1,str_hashed)