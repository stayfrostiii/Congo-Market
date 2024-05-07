# main.py (FastAPI backend)
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Response
from fastapi import Depends, Request
from fastapi import File, Form, UploadFile

from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer, select, or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from ConnectionManager import ConnectionManager
from endpoints.loginEndpoints import create_account, login, add_credit_card, delete_account
from endpoints.itemEndpoints import query_item, item_profile, add_item, search_item
from models import AccountCreate, Login, FriendModel, queryItem, getItemKey, addItem, searchItem, Item, Account, CreditCard, Message
from database import SessionLocal, Base, engine
from messaging.messages import get_username_by_client_id
from endpoints.fileEndpoints import query_Files, queryFiles
import json
from typing import Annotated

from endpoints.friendEndpoints import add_friend_to_account, delete_friend_from_account, fetch_friends_list
import unicodedata
from typing import List, Dict

from messaging.messages import store_message, get_messages
# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, db: Session = Depends(get_db)):
    await manager.connect(websocket)  # Connect client
    try:
        username = get_username_by_client_id(db,client_id)
        while True:
            data = await websocket.receive_text()  
            message_data = json.loads(data)
            message_content = message_data.get("message", "")  # Get the value of "message" or an empty string if not found
            recipient_username = message_data.get("recipient", "")
            sender_id = client_id
            query = db.query(Account).filter(Account.username == recipient_username).first()
            recipient_id = query.user_id
            store_message(sender_id, recipient_id, message_data.get("message", ""))
    except WebSocketDisconnect:
        manager.disconnect(websocket)  # Disconnect client
        await manager.broadcast(f"{client_id} has left the chat")
        
@app.get("/get_message/sender={client_id}&recipient={recipient_name}", response_model=List[Dict[str,str]])
async def get_message_list(client_id: int, recipient_name: str, db: Session = Depends(get_db)):
   recipient_id = db.query(Account).filter(Account.username == recipient_name).first().user_id
   condition_1 = and_(Message.sender_id == client_id, Message.recipient_id == recipient_id)
   condition_2 = and_(Message.sender_id == recipient_id, Message.recipient_id == client_id)
   results = db.query(Message).filter(or_(condition_1,condition_2)).all()
   return [{"sender_username": result.sender.username, "content": result.content} for result in results]

@app.get("/get_name/user={userId}", response_model=str) 
async def get_name(userId: int, db: Session = Depends(get_db)):
    name = db.query(Account).filter(Account.user_id == userId).first()
    return name.username
      
# Endpoint to create a new account with encrypted email, password, and public key
@app.post("/create_account")
async def create_account_handler(account: AccountCreate):
    db = SessionLocal()                 
    return create_account(db, account)

@app.post("/friends/{user_id}")           # Endpoint to add a friend to an account's friends list
async def add_friend_handler(user_id: int, friend: FriendModel, request: Request):
    db = SessionLocal()
    return add_friend_to_account(db, user_id, friend, request)

@app.delete("/friends/{user_id}/{id_number}")     # Endpoint to delete friend FROM account friend list
async def delete_friend_handler(user_id: int, id_number: int):
    db = SessionLocal()
    return delete_friend_from_account(db, user_id, id_number)

@app.get("/friends/{user_id}")                #Endpoint to fetch/get friends list from account's friends list
async def get_friends_list(user_id: int):
    db = SessionLocal()
    return fetch_friends_list(db, user_id)


@app.post("/login")
async def login_handler(login_data: Login, response: Response):
    db = SessionLocal()
    return login(db, login_data, response)  # Pass the login_data object directly

@app.post("/delAccount/{user_id}")
async def delete_account_handler(user_id: int):
    db = SessionLocal()
    return delete_account(db, user_id)

@app.post("/add_card/{user_id}")
async def add_card_handler(user_id: int, credit_card_data: CreditCard):
    db = SessionLocal()
    return add_credit_card(db, user_id, credit_card_data)

@app.post("/query_item")
async def item_handler(item: queryItem):
    db = SessionLocal()
    return query_item(db, item)

@app.post("/item_profile")
async def item_profile_handler(item: getItemKey):
    db = SessionLocal()
    return item_profile(db, item)

@app.post("/add_item")
async def add_item_handler(item: addItem):
    db = SessionLocal()
    return add_item(db, item)

@app.post("/files")
async def file_handler(
    file: Annotated[UploadFile, File()]
    ):
    db = SessionLocal()
    return query_Files(db, file)

@app.post("/owner_item")
async def search_item_handler(item: searchItem):
    db = SessionLocal()
    return search_item(db, item)

@app.get("/search_users", response_model=List[str])
async def search_users(db: Session = Depends(get_db)):
    try:
        # Query all usernames from the database
        users = db.query(Account.username).all()
        # Extract usernames from the result
        usernames = [user[0] for user in users]
        return usernames
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")


