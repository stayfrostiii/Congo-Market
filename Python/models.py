#models.py
from pydantic import BaseModel
from database import Base
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, TEXT
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class AccountCreate(BaseModel):
    email: str
    password: str

    # Pydantic model for login request body
class Login(BaseModel):
    email: str
    password: str

class CreditCard(BaseModel):
    card_number: str
    expiry_date: str
    cvv: str

class FriendModel(BaseModel): #temp table for messaging
    firstName: str
    lastName: str
    idNumber: str
    
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
    user_id = Column(Integer)  # Store user ID as a string
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    salt = Column(String)  # Store public key as a string
    public_key = Column(TEXT)  # New column to store public key
    friends_list = Column(TEXT)
    username = Column(TEXT)
    credit_card = Column(TEXT)
    sent_messages = relationship("Message", back_populates="sender", foreign_keys=[Message.sender_id])
    received_messages = relationship("Message", back_populates="recipient", foreign_keys=[Message.recipient_id])



class queryItem(BaseModel):
    name: str

class getItemID(BaseModel):
    itemID: int

class Item(Base):
    __tablename__ = "item"

    itemkey = Column(String, primary_key = True, index = True)
    name = Column(String)
    desc = Column(String)
    itemID = Column(Integer)
    price = Column(Float)
    time = Column(Float)
    date = Column(Integer)
    owner = Column(Integer)
    distCenter = Column(Integer)


class Node:
    def __init__(self, friend):
        self.friend = friend
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_friend(self, friend):
        new_node = Node(friend)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def display_friends(self):
        current = self.head
        while current:
            print(f"{current.friend.first_name} {current.friend.last_name} ({current.friend.id_number})")
            current = current.next

    def quicksort(self, friends):
        if not friends:
            return []
        else:
            pivot = friends[0]
            less_than_pivot = [friend for friend in friends[1:] if friend.first_name < pivot.first_name]
            greater_than_pivot = [friend for friend in friends[1:] if friend.first_name >= pivot.first_name]
            return self.quicksort(less_than_pivot) + [pivot] + self.quicksort(greater_than_pivot)