# main.py (FastAPI backend)
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from ConnectionManager import ConnectionManager
from endpoints.loginEndpoints import create_account, login 
from endpoints.itemEndpoints import query_item, item_profile
from models import AccountCreate, Login, FriendModel, Friend, Node, LinkedList, queryItem, getItemID, Item
from database import SessionLocal, Base, engine
from messaging.messages import store_message, get_messages
import json
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


manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)  # Connect client
    try:
        while True:
            data = await websocket.receive_text()  # Receive message from client
            # Process the received message, e.g., save it to the database
            message_data = json.loads(data)
            message_content = message_data.get("message", "")  # Get the value of "message" or an empty string if not found
            await manager.broadcast(f"{client_id}: {message_content}")
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

@app.post("/login")
async def login_handler(login_data: Login):
    db = SessionLocal()
    return login(db, login_data)  # Pass the login_data object directly

friend_list = LinkedList()

# Define API endpoints
@app.post("/friends")
async def add_friend(friend: FriendModel):
    friend_list.add_friend(Friend(friend.first_name, friend.last_name, friend.id_number))
    return {"message": "Friend added successfully"}

@app.get("/friends")
async def get_friends():
    friends = []
    current = friend_list.head
    while current:
        friends.append({
            "first_name": current.friend.first_name,
            "last_name": current.friend.last_name,
            "id_number": current.friend.id_number
        })
        current = current.next
    return friends

@app.post("/query_item")
async def item_handler(item: queryItem):
    db = SessionLocal()
    return query_item(db, item)

@app.post("/item_profile")
async def item_profile_handler(item: getItemID):
    db = SessionLocal()
    return item_profile(db, item)
