from pydantic import BaseModel
from database import Base
from sqlalchemy import Column, String, Integer

class AccountCreate(BaseModel):
    email: str
    password: str

    # Pydantic model for login request body
class Login(BaseModel):
    email: str
    password: str

class Account(Base):
    __tablename__ = "account_test"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    public_key = Column(String)  # New column to store public key
    private_key = Column(String)  # New column to store public key