import os
import hashlib
import base64
from cryptography.fernet import Fernet

# Define how heavy we want the math to be
ITERATIONS = 600000 


def generate_salt():
    """Generates a secure, random 16-byte salt."""
    return os.urandom(16)



def derive_master_key(master_password, vault_salt):
    derived = hashlib.pbkdf2_hmac(
        'sha256',
        bytes(master_password, 'utf-8'), # converts to bytes
        vault_salt,
        ITERATIONS
    )

    return base64.urlsafe_b64encode(derived)



def generate_login_hash(master_key, login_salt):
    login_hash = hashlib.pbkdf2_hmac(
        'sha256',
        master_key,
        login_salt,
        ITERATIONS
    )

    return login_hash.hex()



def encrypt_data(plaintext, master_key):
    f = Fernet(master_key)
    return f.encrypt(plaintext.encode('utf-8'))


def decrypt_data(encrypted_text, master_key):
    f = Fernet(master_key)
    return f.decrypt(encrypted_text.decode('utf-8'))