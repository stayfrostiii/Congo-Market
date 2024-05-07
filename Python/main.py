# main.py (FastAPI backend)
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Response
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from ConnectionManager import ConnectionManager
from endpoints.loginEndpoints import create_account, login, add_credit_card, delete_account
from endpoints.itemEndpoints import query_item, item_profile, add_item, search_item
from models import AccountCreate, Login, FriendModel, Node, LinkedList, queryItem, getItemKey, addItem, searchItem, Item, Account, CreditCard

from database import SessionLocal, Base, engine
from messaging.messages import get_username_by_client_id
import json

from endpoints.friendEndpoints import add_friend_to_account, delete_friend_from_account, fetch_friends_list


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
            store_message(sender_id, recipient_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)  # Disconnect client
        await manager.broadcast(f"{client_id} has left the chat")

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

@app.post("/add_item")
async def search_item_handler(item: searchItem):
    db = SessionLocal()
    return search_item(db, item)
