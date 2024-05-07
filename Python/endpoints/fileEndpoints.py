from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from pydantic import BaseModel
from database import Base
import zlib

class queryFiles(BaseModel):
    name: str
    contents: bytes
    userid: int

class files(Base):
    __tablename__ = "files"

    name = Column(String, primary_key=True, index=True)
    contents = Column(LargeBinary)
    size = Column(Integer)
    originalSize = Column(Integer)
    # userid = Column(Integer)

def query_Files(db: Session, item: queryFiles):
    try:
        # Read the contents of the file
        file_contents = item.file.read()
        rle_encoded_contents = encode_file(file_contents)
        # Create a new file object with the file name and contents
        new_file = files(
            name=item.filename,
            contents=rle_encoded_contents,
            size=len(file_contents),
            originalSize=len(rle_encoded_contents)
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

def rle_encode(data):
    encoded_data = bytearray()
    i = 0
    while i < len(data):
        # Count the number of consecutive occurrences of the current value
        count = 1
        while i + count < len(data) and data[i] == data[i + count]:
            count += 1
        # Append the count and value to the encoded data
        encoded_data.append(count)
        encoded_data.append(data[i])
        # Move to the next value
        i += count
    return bytes(encoded_data)

def rle_decode(encoded_data):
    decoded_data = bytearray()
    i = 0
    while i < len(encoded_data):
        # Read the count and value from the encoded data
        count = encoded_data[i]
        value = encoded_data[i + 1]
        # Append the value count times to the decoded data
        decoded_data.extend([value] * count)
        # Move to the next encoded pair
        i += 2
    return bytes(decoded_data)

def encode_file(file_contents):
    try:
        # Ensure that file_contents is bytes data
        if not isinstance(file_contents, bytes):
            raise ValueError("Input data must be bytes")
        
        # Encode the file contents using RLE compression
        encoded_contents = rle_encode(file_contents)
        print("Encoded data:", encoded_contents)  # Debug print
        return encoded_contents
    except Exception as e:
        print("Error in encode_file:", e)
        raise ValueError("Error occurred during file encoding")

def decode_file(file_contents):
    try:
        decoded_contents = rle_decode(file_contents)
        return decoded_contents
    except Exception as e:
        print("Error:", e)
        raise
