import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from Crypto.Util.Padding import pad
import base64

# Configuration
PASSWORD = "YOUR_SECRET_PASSWORD"  # Replace with a strong password
SALT = get_random_bytes(16)  # A random salt for key derivation (Vai eta kintu store kore rakhte hobe noyto ar decrypt kora jabe na)
ENCRYPTION_PATH = ""  # Vai etate jei directory encrypt kora lagbe tar path dite hobe
IV_PATH = ""  # Directory to store IVs

# Key derivation
key = scrypt(PASSWORD.encode(), SALT, 32, N=2**14, r=8, p=1)  # AES-256 key

# Create the IV directory
if not os.path.exists(IV_PATH):
    os.makedirs(IV_PATH)

# Storing the randomly generated salt
with open('salt.bin', 'wb') as salt_file:
    salt_file.write(SALT)

def encrypt_file(file_path):
    cipher = AES.new(key, AES.MODE_CBC)
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Encrypting the data
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    
    # Writing the IV to a separate file
    iv_path = os.path.join(IV_PATH, os.path.basename(file_path) + '.iv')
    with open(iv_path, 'wb') as f:
        f.write(cipher.iv)
    
    # Write the encrypted data back to the original file
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)
    
    print(f'Encrypted: {file_path}')

def encrypt_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path)

# Encrypt the specified directory
encrypt_directory(ENCRYPTION_PATH)

print("Encryption complete.")

print(f"salt = {SALT}")