import psycopg2
from modules.crypto import encrypt_data, decrypt_data
from modules.db import execute_query

class LoginCredentials:
    def __init__(self, id, domain, associated_username, encrypted_pass):
        self.id = id
        self.domain = domain
        self.associated_username = associated_username
        self.encrypted_pass = encrypted_pass


def add_login_credentials(user_id, domain, username, plaintext_password, master_key):
    encrypted_password = encrypt_data(plaintext_password, master_key)

    query = "INSERT INTO passwords (user_id, domain, associated_username, encrypted_pass) VALUES (%s, %s, %s, %s);"

    execute_query(
        query,
        (
            user_id,
            domain,
            username,
            psycopg2.Binary(encrypted_password)
        ),
        fetch=False
    )
    print(f"Successfully added secure record for {domain}!")


def get_login_credentials(user_id):
    query = "SELECT id, domain, associated_username, encrypted_pass FROM passwords WHERE user_id = %s;"
    result = execute_query(query, (user_id,), fetch=True)

    if not result: 
        return None
    else:
        id, domain, associated_username, encrypted_pass = result[0]
        return LoginCredentials(id, domain, associated_username, encrypted_pass)


def decrypt_password(encrypted_password, master_key):
    if isinstance(encrypted_password, memoryview):
        encrypted_password = bytes(encrypted_password)
    decrypted_bytes = decrypt_data(encrypted_password, master_key)
    return decrypted_bytes.decode('utf-8')