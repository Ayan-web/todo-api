from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import bson.objectid
import datetime
import json

load_dotenv()
# client = AsyncIOMotorClient('localhost',27017)
client = AsyncIOMotorClient(os.environ['MONGO_URL'])

user = client.test.user
todo = client.test.todo

# user 
#################################

class User:
    def __init__(self,username,email,password,disabled=False) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.disabled = disabled

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(username:str,email:str,password:str,disabled:bool=False):
    hash_password = pwd_context.hash(password) 
    document = User(username,email,hash_password,disabled)
    await user.insert_one(vars(document))

###### object id handler
def my_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    else:
        raise TypeError(x)

async def get_user(username:str):
    document = await user.find_one({'username':username})
    newDocument =json.dumps(document,default=my_handler)     
    newDocument = json.loads(newDocument)
    newDocument['id'] = newDocument.pop('_id')
    # print(newDocument['id'])
    return newDocument

# todo 
#########################################

class Todo:
    def __init__(self,text:str,userId:str,isCompleted:bool=False) -> None:
        self.text = text
        self.isCompleted = isCompleted
        self.userId = userId

async def add_todo(userId:str,text:str,isCompleted:bool=False):
    newtodo = Todo(text,userId,isCompleted)
    await todo.insert_one(vars(newtodo))
    return True

async def get_all_todos(userId:str):
    returnlist:list=[]
    async for document in todo.find({'userId':userId}):
        newDocument =json.dumps(document,default=my_handler)     
        newDocument = json.loads(newDocument)
        newDocument['id'] = newDocument.pop('_id')
        newDocument.pop('userId')
        returnlist.append(newDocument)
    return returnlist



async def remove_todo(todo_id:str):
    result = await todo.delete_one({'_id':bson.objectid.ObjectId(todo_id)})
    if not result:
        return False
    return True

async def toggle_todo(todo_id:str):
    document = await todo.find_one({'_id':bson.objectid.ObjectId(todo_id)})
    # print(not document['isCompleted'])
    newtoggle = not document['isCompleted']
    result = await todo.update_one({'_id':bson.objectid.ObjectId(todo_id)},{'$set':{'isCompleted':newtoggle}})
    if not result:
        return False
    return True

async def change_todo_text(todo_id:str,new_text:str):
    result = await todo.update_one({'_id': bson.objectid.ObjectId(todo_id)}, {'$set': {'text':new_text} })
    if result :
        return True
    return False

