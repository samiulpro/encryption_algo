import os
import hashlib

# Configuration
DIRECTORY_PATH = '/home/kali/project_hashecrypt/testdir/' # This is the path where you want to encrypt
key = 'STEPDOWNHASINA' # Create a plain text password

# xor algorithm functinality
def xor(var, key):
    return bytes(a ^ b for a, b in zip(var, key))


def encrypt(file_path):
    cipher = bytes()
    
    with open(file_path, 'rb') as f:
        data = f.read()
        for j in range(len(data)):
            cipher += xor(int.to_bytes(data[j]), key=key.encode('utf-8'))
        
        with open(file_path, 'wb') as fe:
            fe.write(cipher)
            cipher = bytes()
            fe.close()
                
        print(f'{file_path} - Encrypted')


def decrypt_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt(file_path)
            

decrypt_directory(DIRECTORY_PATH)