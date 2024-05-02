from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./congo.db"

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Base class for declarative models
Base = declarative_base()

class Account(Base):
    __tablename__ = "account_test"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    public_key = Column(String)  # New column to store public key
    private_key = Column(String)  # New column to store public key