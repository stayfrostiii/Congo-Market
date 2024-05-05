from pydantic import BaseModel
from database import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
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

class FriendModel(BaseModel):   #For Friend's List
    first_name: str
    last_name: str
    id_number: int

class Account(Base):
    __tablename__ = "account_test"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    public_key = Column(String)  # New column to store public key
    private_key = Column(String)  # New column to store public key

#temporary table for testing the messaging
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("account_test.id"))
    recipient_id = Column(Integer, ForeignKey("account_test.id"))
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.now)

    sender = relationship("Account", foreign_keys=[sender_id])
    recipient = relationship("Account", foreign_keys=[recipient_id])

class Item(Base):
    __tablename__ = "item"

    itemkey = Column(String, primary_key = True, index = True)
    name = Column(String)
    desc = Column(String)
    itemID = Column(Integer)
    price = Column(Float)
    time = Column(Float)
    date = Column(Integer)

class Friend:
    def __init__(self, first_name, last_name, id_number):
        self.first_name = first_name
        self.last_name = last_name
        self.id_number = id_number

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