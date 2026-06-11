import re
import psycopg2
from modules.crypto import generate_salt, derive_master_key, generate_login_hash
from modules.db import execute_query
from modules.exceptions import InvalidCredentials, UserAlreadyExists, UserDoesNotExist, InvalidPassword

class UserCredentials:
    def __init__(self, id, username, master_pass_hash, login_salt, vault_salt, master_key=None):
        self.id = id
        self.username = username
        self.master_pass_hash = master_pass_hash
        self.login_salt = login_salt
        self.vault_salt = vault_salt
        self.master_key = master_key


def get_new_user_credentials(username, password):
    login_salt = generate_salt()
    vault_salt = generate_salt()

    master_key = derive_master_key(password, vault_salt)
    login_hash = generate_login_hash(master_key, login_salt)

    user = UserCredentials(None, username, login_hash, login_salt, vault_salt, master_key)
    return user


def validate_password(password):
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character.")


def register(username, password):
    validate_password(password)
    user_already_exists = user_exists(username)
    if user_already_exists:
        raise UserAlreadyExists("User already exists. Please choose a different username.")
    user = get_new_user_credentials(username, password)
    query = "INSERT INTO users (username, master_pass_hash, login_salt, vault_salt) VALUES (%s, %s, %s, %s);"
    execute_query(query, 
                (
                      user.username, 
                      user.master_pass_hash, 
                      psycopg2.Binary(user.login_salt), 
                      psycopg2.Binary(user.vault_salt),
                ),
                False)
    

def login(username, password_input):
    query = "SELECT id, master_pass_hash, login_salt, vault_salt FROM users WHERE username = %s;" 
    result = execute_query(query,
                  (username,),
                  True
                  )
    if not result:
        raise UserDoesNotExist()
    
    user_id, master_pass_hash, login_salt, vault_salt = result[0]

    computed_master_key = derive_master_key(password_input, bytes(vault_salt))
    computed_login_hash = generate_login_hash(computed_master_key, bytes(login_salt))

    # Verification
    if computed_login_hash == master_pass_hash:
        print("Access granted!")
        return UserCredentials(user_id, username, master_pass_hash, login_salt, vault_salt, computed_master_key)
    else:
        raise InvalidPassword()


def user_exists(username):
    query = "SELECT id FROM users WHERE username = %s;"
    result = execute_query(query, (username,), True)
    return bool(result)

    
