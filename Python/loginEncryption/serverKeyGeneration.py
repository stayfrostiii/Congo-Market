import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Generate a private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Serialize the private key to PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Generate the corresponding public key
public_key = private_key.public_key()

# Serialize the public key to PEM format
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Define the path to the key vault directory
KEY_VAULT_DIR = "./key_vault"

# Ensure the key vault directory exists
if not os.path.exists(KEY_VAULT_DIR):
    os.makedirs(KEY_VAULT_DIR)

# Define the path to store the private key
PRIVATE_KEY_PATH = os.path.join(KEY_VAULT_DIR, "private_key.pem")

# Define the path to store the public key
PUBLIC_KEY_PATH = os.path.join(KEY_VAULT_DIR, "public_key.pem")

# Write the private key to the key vault
with open(PRIVATE_KEY_PATH, "wb") as private_key_file:
    private_key_file.write(private_pem)

# Write the public key to the key vault
with open(PUBLIC_KEY_PATH, "wb") as public_key_file:
    public_key_file.write(public_pem)

# Print confirmation message
print("Private and public keys stored securely in the key vault.")
