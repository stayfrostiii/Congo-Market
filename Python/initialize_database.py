from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import Account
from database import SessionLocal

# Function to initialize user_id values
def initialize_user_ids():
    session = SessionLocal()
    try:
        # Add user_id values from 1000000 to 1999999
        for i in range(1000000, 2000000):
            account = Account(id=i)
            session.add(account)
        session.commit()
        print("user_id values initialized successfully")
    except Exception as e:
        session.rollback()
        print("Error:", e)
    finally:
        session.close()
        

# Call the function to initialize user_id values
initialize_user_ids()
