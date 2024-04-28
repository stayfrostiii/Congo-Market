from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import AccountCreate, Login
from database.database import Account

def create_account(db: Session, account: AccountCreate):
    try:
        # Check if email already exists
        if db.query(Account).filter(Account.email == account.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new account
        new_account = Account(email=account.email, password=account.password)
        db.add(new_account)
        db.commit()
        return {"message": "Account created successfully"}
    except Exception as e:
        db.rollback()
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

def login(db: Session, login_data: Login):  # Updated to accept Login model
    try:
        # Query the database for the user with the provided email
        user = db.query(Account).filter(Account.email == login_data.email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Compare the email and password with the provided credentials
        if user.email != login_data.email or user.password != login_data.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # If the credentials match, return a success message
        return {"message": "Login successful"}
    except HTTPException as http_error:
        # Re-raise HTTPException to return specific error responses
        raise http_error
    except Exception as e:
        # Log and handle other exceptions
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()
