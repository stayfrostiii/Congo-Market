from sqlalchemy.orm import Session, Column, Integer, String, bytes
from fastapi import HTTPException
from pydantic import BaseModel
from database import Base

class queryFiles(BaseModel):
    name: str
    contents: bytes
    userid: int

class files(Base):
    __tablename__ = "files"

    FileID = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contents = Column(bytes)
    userid = Column(Integer)

def query_Files(db: Session, item: queryFiles):
    try:
        new_file = files(name=item.name, contents=item.contents, userid=item.userid)
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
        
        return {"message": "File created successfully"}

    except Exception as e:
        # Log and handle exceptions
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()