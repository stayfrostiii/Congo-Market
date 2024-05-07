import jwt
from datetime import datetime, timedelta
import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


# Define the secret key for JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time


def create_access_token(user_id: str) -> str:
    """
    Generate a JWT token with the provided user ID.
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def encrypt_message(public_key, message):
    print("Type of public_key in encrypt_message:", type(public_key))  # Debug print
    # Load the public key
    public_key = serialization.load_pem_public_key(public_key)
    
    # Ensure message is encoded to bytes
    message_bytes = message.encode()
    print("Type of message in encrypt_message:", type(message_bytes))  # Debug print

    # Encrypt the message using the public key
    encrypted_message = public_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return encrypted_message

def encrypt_message_str(public_key, message):
    # Load the public key
    public_key = serialization.load_pem_public_key(public_key)
    
    # Ensure message is encoded to bytes
    message_bytes = message.encode()

    # Encrypt the message using the public key
    encrypted_message = public_key.encrypt(
        message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Convert the encrypted message to a base64-encoded string
    encrypted_message_str = base64.b64encode(encrypted_message).decode()
    
    return encrypted_message_str


def decrypt_message(private_key, encrypted_message):
    # Deserialize the private key from PEM format
    private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Load the private key
    private_key = serialization.load_pem_private_key(private_key, password=None)

    # Decrypt the message using the private key
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_message.decode()

def read_server_keys(public_key_path, private_key_path):
    try:
        # Read the server's public key from the PEM file
        with open(public_key_path, "rb") as public_key_file:
            public_key_bytes = public_key_file.read()
            print("Content of public key PEM file:", public_key_bytes)
            # Remove the following line which loads the key into RSAPublicKey object
            # public_key = serialization.load_pem_public_key(public_key_bytes)
            print("Type of public_key:", type(public_key_bytes))  # Print the type of the public key object

        # Read the server's private key from the PEM file
        with open(private_key_path, "rb") as private_key_file:
            private_key_bytes = private_key_file.read()
            private_key = serialization.load_pem_private_key(
                private_key_bytes,
                password=None  # No password protection on the private key
            )

        return public_key_bytes, private_key
    except Exception as e:
        print("Error reading server keys:", e)
        raise  # Reraise the exception for higher-level handling



