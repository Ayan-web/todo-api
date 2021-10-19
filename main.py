from datetime import datetime, timedelta
# from pydantic.fields import Field
from dotenv import load_dotenv
import os
import db
from jose import JWTError, jwt
# from bson import ObjectId
from typing import Optional
from fastapi import FastAPI,Depends,HTTPException,status
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

app = FastAPI()



## somebootstrap variable  
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None

class Todo(BaseModel):
    todo : str
    isComplete : bool

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#                            this is  for auth
#################################################################################################
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password) 

class UserInDB(User):
    password: str
    id:Optional[str] = None

async def get_user(username):
    user = await db.get_user(username)
    if not user :
        False
    return  UserInDB(**user)



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ['SECRET_KEY'], algorithm=os.environ['ALGORITHM'])
    return encoded_jwt

async def authenticate_user( username: str, password: str):
    user = await get_user( username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            )
    try:
        payload = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=[os.environ['ALGORITHM']])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user





#               routes 
#################################################################################################

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # print(form_data.password)
    # print("was here")
    user = await authenticate_user( form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/create")
async def create_user(user:UserInDB):
    await db.create_user(user.username,user.email,user.password,user.disabled)
    return 'created succesfully'

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post("/todo/add")
async def create_todo(todo:Todo,current_user: UserInDB = Depends(get_current_active_user)):
    # print(current_user)
    result = await db.add_todo(current_user.id,todo.todo,todo.isComplete)
    if(not result):
        return 'somthing went wrong '
    return "todo added"

@app.get("/todo/all")
async def get_all_todos(current_user:UserInDB = Depends(get_current_active_user)):
    return await db.get_all_todos(current_user.id)

@app.put("/todo/text/{todo_id}")
async def read_item(todo_id: str,todo_text:str,current_user:User=Depends(get_current_active_user)):
    result = await db.change_todo_text(todo_id,todo_text)
    if not result:
        return 'somthing went wrong'
    return 'todo updated'

@app.put("/todo/toggleComplete/{todo_id}")
async def toggle_complete(todo_id:str):
    result = await db.toggle_todo(todo_id)
    if not result:
        return 'something went wrong'
    return 'todo updated'

@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id:str):
    result = await db.remove_todo(todo_id)
    if not result:
        return 'something went wrong'
    return 'todo delete'
