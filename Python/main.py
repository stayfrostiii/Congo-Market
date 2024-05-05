# main.py (FastAPI backend)
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Response
from fastapi import Depends
from sqlalchemy.orm import Session
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
from endpoints.friendEndpoints import add_friend_to_account

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
            # Then broadcast the message to all connected clients
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)  # Disconnect client
        await manager.broadcast(f"Client {client_id} has left the chat")

# Endpoint to create a new account with encrypted email, password, and public key
@app.post("/create_account")
async def create_account_handler(account: AccountCreate):
    db = SessionLocal()
    return create_account(db, account)

# Endpoint to add a friend to an account's friends list
@app.post("/friends")
async def add_friend_handler(friend: FriendModel):
    db = SessionLocal()
    return add_friend_to_account(db, friend)

@app.post("/login")
async def login_handler(login_data: Login, response: Response):
    db = SessionLocal()
    return login(db, login_data, response)  # Pass the login_data object directly


@app.post("/query_item")
async def item_handler(item: queryItem):
    db = SessionLocal()
    return query_item(db, item)

@app.post("/item_profile")
async def item_profile_handler(item: getItemID):
    db = SessionLocal()
    return item_profile(db, item)
