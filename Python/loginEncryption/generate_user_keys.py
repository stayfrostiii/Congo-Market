import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def email_to_user_id(email):
    """
    Generate a user ID from an email address.
    """
    # Consider using a more secure hashing algorithm
    hash_value = hash(email)
    user_id = (hash_value % 1000000) + 1000000
    return user_id

def generate_user_keys(user_id):
    """
    Generate RSA key pair for a user and store the private key on a USB drive.
    Return the PEM-encoded public key.
    """
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Extract public key
    public_key = private_key.public_key()

    # Serialize the private key to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Specify the path to the USB drive
    usb_drive_path = "C:\\Users\\Jeremy\\Desktop\\keys"
    #usb_drive_path = "D:\\"
    # usb_drive_path = "C:\\Users\\SunHa\\OneDrive\\Desktop\\CMPE-130AshSetup"
    # usb_drive_path = "D:\\SJSU\\CMPE_130\\Congo\\Keys"


    # Specify the path to the user's private key directory on the USB drive
    user_private_key_dir = os.path.join(usb_drive_path, "private_keys", str(user_id))

    # Ensure the user's private key directory exists
    if not os.path.exists(user_private_key_dir):
        os.makedirs(user_private_key_dir)

    # Define the path to store the user's private key
    private_key_filename = f"private_key_{user_id}.pem"
    user_private_key_path = os.path.join(user_private_key_dir, private_key_filename)

    # Write the user's private key to the directory
    with open(user_private_key_path, "wb") as private_key_file:
        private_key_file.write(private_pem)

    # Generate the PEM-encoded public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Return the PEM-encoded public key
    return public_pem.decode()

def read_private_key(user_id):
    # Specify the path to the USB drive
    usb_drive_path = "C:\\Users\\Jeremy\\Desktop\\keys"
    
    #usb_drive_path = "D:\\"
    # usb_drive_path = "D:\\SJSU\\CMPE_130\\Congo\\Keys"
    
    # Specify the path to the user's private key directory on the USB drive
    user_private_key_dir = os.path.join(usb_drive_path, "private_keys", str(user_id))

    # Define the path to the user's private key file
    private_key_filename = f"private_key_{user_id}.pem"
    user_private_key_path = os.path.join(user_private_key_dir, private_key_filename)

    # Read the private key from the file
    with open(user_private_key_path, "rb") as private_key_file:
        private_key_data = private_key_file.read()
    
    # Deserialize and return the private key
    private_key = serialization.load_pem_private_key(private_key_data, password=None)
    return private_key

# Example usage
# email = "example@example.com"
# user_id = email_to_user_id(email)
# user_public_key = generate_user_keys(user_id)
# print(user_public_key)
