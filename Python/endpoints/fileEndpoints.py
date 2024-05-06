from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import BaseModel
from database import Base

class queryFiles(BaseModel):
    name: str
    contents: bytes
    userid: int

class files(Base):
    __tablename__ = "files"

    name = Column(String, primary_key=True, index=True)
    contents = Column(LargeBinary)
    # userid = Column(Integer)

def query_Files(db: Session, item: queryFiles):
    try:
        # Read the contents of the file
        file_contents = item.file.read()

        # Create a new file object with the file name and contents
        new_file = files(
            name=item.filename, 
            contents=file_contents
            # userid=item.userid
        )

        # Add the new file to the database session and commit the transaction
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


    