# main.py (FastAPI backend)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from endpoints.loginEndpoints import create_account, login
from models import AccountCreate, Login
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
