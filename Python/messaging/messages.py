# message_utils.py

from datetime import datetime
from sqlalchemy.orm import Session
from models import Message
from database import SessionLocal

def store_message(sender_id: int, recipient_id: int, content: str):
    # Open a database session
    db = SessionLocal()
    try:
        # Create a new Message object
        message = Message(sender_id=sender_id, recipient_id=recipient_id, content=content, timestamp=datetime.now())
        # Add the message to the session
        db.add(message)
        # Commit the transaction
        db.commit()
    except Exception as e:
        # Rollback the transaction in case of an error
        db.rollback()
        raise e
    finally:
        # Close the session
        db.close()

def get_messages(sender_id: int, recipient_id: int):
    # Open a database session
    db = SessionLocal()
    try:
        # Query the Message table
        messages = db.query(Message).filter(Message.sender_id == sender_id, Message.recipient_id == recipient_id).all()
        # Extract the required information from the messages
        message_data = [{"sender_id": message.sender_id, "recipient_id": message.recipient_id, "content": message.content, "timestamp": message.timestamp} for message in messages]
        return message_data
    finally:
        # Close the session
        db.close()
