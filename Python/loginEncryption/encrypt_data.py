import os
import hashlib
import secrets

def generate_salt():
    """
    Generate a random salt value.
    """
    return secrets.token_bytes(2)  # Generate a 16-byte (128-bit) random salt

def hash_password(password, salt):
    """
    Hash a password with a salt using SHA-256.
    """
    # Combine the password and salt
    salted_password = salt + password.encode()
    
    # Hash the salted password using SHA-256
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    
    return hashed_password



# Example usage
#password = "example_password"
#salt = generate_salt()
#hashed_password = hash_password(password, salt)
#print("Hashed Password:", hashed_password)
