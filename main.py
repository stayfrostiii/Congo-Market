# main.py (FastAPI backend)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from loginFunctions.encryption import generate_key_pair, encrypt_message, decrypt_message  # Importing encryption functions
from endpoints.loginEndpoints import create_account, login
from models import AccountCreate, Login
# Use SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./congo.db"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create SQLAlchemy session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Define database model
class Account(Base):
    __tablename__ = "account_test"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    public_key = Column(String)  # New column to store public key
    private_key = Column(String)  # New column to store public key

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
