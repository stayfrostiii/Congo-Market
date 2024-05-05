# api/messages.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Message, Account

router = APIRouter()

class MessageCreate(BaseModel):
    recipient_id: int
    content: str

@router.post("/send_message/{sender_id}")
async def send_message_handler(sender_id: int, message: MessageCreate, db: Session = SessionLocal()):
    recipient = db.query(Account).filter(Account.id == message.recipient_id).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    db_message = Message(sender_id=sender_id, recipient_id=message.recipient_id, content=message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Return a dictionary representing the message
    return {"id": db_message.id, "sender_id": db_message.sender_id, "recipient_id": db_message.recipient_id, "content": db_message.content}

@router.get("/messages/{recipient_id}")
async def get_messages_handler(recipient_id: int, db: Session = SessionLocal()):
    recipient = db.query(Account).filter(Account.id == recipient_id).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    messages = db.query(Message).filter(Message.recipient_id == recipient_id).all()
    
    # Convert messages to a list of dictionaries
    messages_data = [{"id": message.id, "sender_id": message.sender_id, "recipient_id": message.recipient_id, "content": message.content} for message in messages]
    
    return messages_data

