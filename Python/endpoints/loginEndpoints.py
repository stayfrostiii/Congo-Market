from sqlalchemy.orm import Session
from sqlalchemy import BLOB, exists
from fastapi import Cookie, Depends, HTTPException, Response, status
from models import AccountCreate, Login, Account, CreditCard
from loginEncryption.generate_user_keys import generate_user_keys, email_to_user_id, read_private_key
from loginEncryption.encrypt_data import generate_salt, hash_password
from loginEncryption.token_authentication import create_access_token, encrypt_message, decrypt_message, read_server_keys, encrypt_message_str


import traceback

def quadratic_probe(db: Session, user_id: int):
    i = 0
    while True:
        # Calculate the next index using quadratic probing
        index = (user_id + i * i) % 1000000 + 1000000
        # Check if the index is available (not occupied or deleted)
        existing_account = db.query(Account).filter(Account.id == index).first()
        if existing_account.status not in [1, 2]:
            return index
        # Increment the probe sequence
        i += 1


def create_account(db: Session, account: AccountCreate):
    try:
        # Check if email already exists
        if db.query(Account).filter(Account.email == account.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Generate user ID from email
        user_id = email_to_user_id(account.email)

        # Print the generated user_id
        print("Generated user_id:", user_id)
        
        # Generate salt for password hashing
        salt = generate_salt()
        
        # Hash password with salt
        hashed_password = hash_password(account.password, salt)
        
        # Check if the generated user ID already exists
        existing_account = db.query(Account).filter(Account.id == user_id).first()
        if existing_account:
            # If user ID exists, perform quadratic probing to find an available ID
            user_id = quadratic_probe(db, user_id)

        # Generate RSA key pair
        public_key_pem = generate_user_keys(user_id)
        
        # Check if the generated user ID already exists
        existing_account = db.query(Account).filter(Account.id == user_id).first()
        if existing_account:
            # If user ID exists, perform quadratic probing to find an available ID
            user_id = quadratic_probe(db, user_id)
        
        # Create new account with hashed password, salt, and user ID
        new_account = Account(id=user_id, status = 1, user_id = user_id, email=account.email, hashed_password=hashed_password, salt=salt, public_key=public_key_pem, username = account.username)
        db.merge(new_account)  # Use merge instead of add
        db.commit()
        return {"message": "Account created successfully", "token": str(user_id)}
    except Exception as e:
        db.rollback()
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()




def login(db: Session, login_data: Login, response: Response):
    try:
        # Query the database for the user with the provided email
        user = db.query(Account).filter(Account.email == login_data.email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if account status is equal to 2
        if user.status == 2:
            raise HTTPException(status_code=403, detail="Account is disabled")

        # Hash the provided password with the user's salt
        hashed_password = hash_password(login_data.password, user.salt)
        
        # Compare the hashed password with the stored hashed password
        if user.hashed_password != hashed_password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Generate a JWT token with the user's ID
        access_token = create_access_token(user.user_id)
        
        # Encrypt the token using the user's public key
        encrypted_token = encrypt_message(user.public_key.encode(), access_token)
        
        # Decrypt the encrypted token using the user's private key
        private_key = read_private_key(user.user_id)
        print("Type of private key:", type(private_key))
        decrypted_token = decrypt_message(private_key, encrypted_token)
        print("Type of decrypted token:", type(decrypted_token))
        # Compare the original token with the decrypted token
        if access_token != decrypted_token:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # If the credentials match, return a success message along with the token
        return {"message": "Login successful", "token": str(user.user_id)}

    except HTTPException as http_error:
        # Re-raise HTTPException to return specific error responses
        raise http_error
    except Exception as e:
        # Log and handle other exceptions
        print("Error:", e)
        traceback.print_exc()  # Print traceback for detailed error information
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()
"""
def add_information(db: Session, data_model, information):
    try:
        # Validate the input data
        if not information:
            raise HTTPException(status_code=400, detail="Information is required")
        
        # Create a new record in the database for the provided information
        new_information = data_model(**information)
        db.add(new_information)
        db.commit()
        return {"message": "Information added successfully"}
    except HTTPException as http_error:
        # Re-raise HTTPException to return specific error responses
        raise http_error
    except Exception as e:
        # Log and handle other exceptions
        print("Error:", e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

"""
def add_credit_card(db: Session, user_id: int, credit_card_data: CreditCard):
    try:
        # Retrieve the account with the provided user ID
        account = db.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Validate credit card data here if needed
        
        # Concatenate credit card information into a string
        credit_card_info = "|".join([
            credit_card_data.cardNumber,
            credit_card_data.expiryDate,
            credit_card_data.cvv
        ])
        
        # Specify paths to the public and private key files
        public_key_path = "key_vault/public_key.pem"
        private_key_path = "key_vault/private_key.pem"

        # Read the server's public and private keys
        public_key, private_key = read_server_keys(public_key_path, private_key_path)
        
        # Encrypt the credit card information
        encrypted_info = encrypt_message_str(public_key, credit_card_info)
        print("Type of encrypted_info:", type(encrypted_info))  # Debug print
        print("Content of encrypted_info:", encrypted_info)  # Debug print
        
        # Store the encrypted information in the database
        account.credit_card = encrypted_info
        
        # Commit the transaction
        db.commit()
        
        return {"message": "Credit card information added successfully"}
    except HTTPException as http_error:
        # Re-raise HTTPException to return specific error responses
        raise http_error
    except Exception as e:
        db.rollback()
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()





def get_credit_card_data(db: Session, user_id: int):
    try:
        # Retrieve the account with the provided user ID
        account = db.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        # Decrypt the encrypted credit card information
        encrypted_credit_card_info = account.encrypted_credit_card_info
        if not encrypted_credit_card_info:
            raise HTTPException(status_code=404, detail="Credit card information not found")

        private_key_path = "./key_vault/private_key.pem"
        # Call the function to read the server's private key
        private_key = read_private_key(private_key_path)

        # Decrypt the credit card information using the private key
        decrypted_credit_card_info = decrypt_message(private_key, encrypted_credit_card_info)

        # Split the decrypted string into individual credit card fields
        card_number, card_holder_name, expiration_date, cvv = decrypted_credit_card_info.split("|")

        return {
            "card_number": card_number,
            "card_holder_name": card_holder_name,
            "expiration_date": expiration_date,
            "cvv": cvv
        }
    except HTTPException as http_error:
        # Re-raise HTTPException to return specific error responses
        raise http_error
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()


def delete_account(db: Session, user_id: int):
    try:
        # Retrieve the account with the provided user ID
        account = db.query(Account).filter(Account.user_id == user_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Store the encrypted information in the database
        account.status = 2
        
        # Commit the transaction
        db.commit()
        
        return {"message": "Account Deleted"}
    except Exception as e:
        db.rollback()
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()