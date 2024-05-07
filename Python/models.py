#models.py
from pydantic import BaseModel
from database import Base
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, TEXT, BLOB
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class AccountCreate(BaseModel):
    email: str
    password: str
    username: str

    # Pydantic model for login request body

class Login(BaseModel):
    email: str
    password: str
    
class CreditCard(BaseModel):
    cardNumber: str
    expiryDate: str
    cvv: str

class FriendModel(BaseModel): #temp table for messaging
    firstName: str
    lastName: str
    idNumber: str

class queryItem(BaseModel):
    searchV: str

class getItemKey(BaseModel):
    itemID: int

class addItem(BaseModel):
    name: str
    desc: str
    price: str
    tags: str
    owner: int

class searchItem(BaseModel):
    itemkey: str

#temp table for messaging
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("account_test.id"))
    recipient_id = Column(Integer, ForeignKey("account_test.id"))
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.now)

    sender = relationship("Account", back_populates="sent_messages", foreign_keys=[sender_id])
    recipient = relationship("Account", back_populates="received_messages", foreign_keys=[recipient_id])

class Account(Base):
    __tablename__ = "account_test"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer)
    user_id = Column(Integer)  # Store user ID as a string
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    salt = Column(String)  # Store public key as a string
    public_key = Column(String)  # New column to store public key
    friends_list = Column(TEXT)
    username = Column(TEXT)
    credit_card = Column(TEXT)

    sent_messages = relationship("Message", back_populates="sender", foreign_keys=[Message.sender_id])
    received_messages = relationship("Message", back_populates="recipient", foreign_keys=[Message.recipient_id])

class Item(Base):
    __tablename__ = "item"

    itemkey = Column(String, primary_key = True, index = True)
    tags = Column(String)
    name = Column(String)
    desc = Column(String)
    itemID = Column(Integer)
    price = Column(Float)
    time = Column(String)
    date = Column(String)
    owner = Column(Integer)
    distCenter = Column(String)
    pageVisits = Column(Float)

