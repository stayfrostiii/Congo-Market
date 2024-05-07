# main.py (FastAPI backend)
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Response
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer, select, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from ConnectionManager import ConnectionManager
from endpoints.loginEndpoints import create_account, login, add_credit_card
from endpoints.itemEndpoints import query_item, item_profile, add_item, search_item
from models import AccountCreate, Login, FriendModel, Node, LinkedList, queryItem, getItemKey, addItem, searchItem, Item, Account, CreditCard
from database import SessionLocal, Base, engine
from messaging.messages import get_username_by_client_id
import json
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
            data = await websocket.receive_text()  # Receive message from client
            # Process the received message, e.g., save it to the database
            message_data = json.loads(data)
            message_content = message_data.get("message", "")  # Get the value of "message" or an empty string if not found
            await manager.broadcast(f"{username}: {message_content}")
            sender_id = client_id
            recipient_id = client_id
            store_message(sender_id, recipient_id, message_data.get("message", ""))
    except WebSocketDisconnect:
        manager.disconnect(websocket)  # Disconnect client
        await manager.broadcast(f"{client_id} has left the chat")
        
# @app.get("/get_message/sender={client_id}&recipient={recipient_name}", response_model= List[str])
# async def get_message_list(client_id: int, recipient_name: str, db: Session = Depends(get_db)):
#     recipient = db.query(Account).filter(Account.username == recipient_name).first()
#     if recipient:
#         recipient_id = recipient.user_id
#         # Query the Message table using the sender ID and recipient ID
#         query = db.query(Message).filter(Message.sender_id == client_id, Message.recipient_id == recipient_id).all()
#         message_list = [message.content for message in query]
#         # Return messages as a list of strings
#         return message_list  # Access the content attribute in the result tuple
#     else:
#         # If recipient is not found, return an empty list
#         return []
 
@app.get("/get_message/sender={client_id}&recipient={recipient_name}", response_model=Dict[str, List[str]])
async def get_message_list(client_id: int, recipient_name: str, db: Session = Depends(get_db)):
    recipient = db.query(Account).filter(Account.username == recipient_name).first()
    if recipient:
        recipient_id = recipient.user_id
        # Join Message and Account tables to get messages along with sender usernames
        query = db.query(Message, Account).join(Account, Message.sender_id == Account.user_id).filter(Message.sender_id == client_id, Message.recipient_id == recipient_id).all()
        
        # Construct the dictionary with usernames and corresponding messages
        message_dict = {}
        for message, account in query:
            username = account.username
            if username not in message_dict:
                message_dict[username] = []
            message_dict[username].append(message.content)

        return message_dict
    else:
        # If recipient is not found, return an empty dictionary
        return {}   
    

# Endpoint to create a new account with encrypted email, password, and public key
@app.post("/create_account")
async def create_account_handler(account: AccountCreate):
    db = SessionLocal()
    return create_account(db, account)

@app.post("/friends")           # Endpoint to add a friend to an account's friends list
async def add_friend_handler(friend: FriendModel, request: Request):
    db = SessionLocal()
    return add_friend_to_account(db, friend, request)

@app.delete("/friends/{id_number}")     #End point to delete friend FROM account friend list
async def delete_friend_handler(id_number: int, request: Request):
    db = SessionLocal()
    return delete_friend_from_account(db, id_number, request)

@app.get("/friends")                #Endpoint to fetch/get friends list from account's friends list
async def get_friends_list(request: Request):
    db = SessionLocal()
    return fetch_friends_list(db, request)


@app.post("/login")
async def login_handler(login_data: Login, response: Response):
    db = SessionLocal()
    return login(db, login_data, response)  # Pass the login_data object directly

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

@app.post("/add_item")
async def search_item_handler(item: searchItem):
    db = SessionLocal()
    return search_item(db, item)

