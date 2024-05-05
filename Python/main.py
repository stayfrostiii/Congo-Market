# main.py (FastAPI backend)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from endpoints.loginEndpoints import create_account, login 
from endpoints.itemEndpoints import query_item, item_profile
from models import AccountCreate, Login, FriendModel, Friend, Node, LinkedList, queryItem, getItemID, Item
from database import SessionLocal, Base, engine

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
