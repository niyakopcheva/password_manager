import os
import hashlib
import base64

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