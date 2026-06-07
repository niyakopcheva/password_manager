import psycopg2
from modules.crypto import generate_salt, derive_master_key, generate_login_hash
from modules.db import execute_query

class UserCredentials:
    def __init__(self, username, master_pass_hash, login_salt, vault_salt):
        self.username = username
        self.master_pass_hash = master_pass_hash
        self.login_salt = login_salt
        self.vault_salt = vault_salt


def get_new_user_credentials(username, password):
    login_salt = generate_salt()
    vault_salt = generate_salt()

    master_key = derive_master_key(password, vault_salt)
    login_hash = generate_login_hash(master_key, login_salt)

    user = UserCredentials(username, login_hash, login_salt, vault_salt)
    return user


def register(username, password):
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
    query = "SELECT master_pass_hash, login_salt, vault_salt FROM users WHERE username = %s;" 
    result = execute_query(query,
                  (username,),
                  True
                  )
    if not result:
        print("User not found!")
        return None
    
    master_pass_hash, login_salt, vault_salt = result[0]

    computed_master_key = derive_master_key(password_input, bytes(vault_salt))
    computed_login_hash = generate_login_hash(computed_master_key, bytes(login_salt))

    # Verification
    if computed_login_hash == master_pass_hash:
        print("Access granted!")
        return UserCredentials(username, master_pass_hash, login_salt, vault_salt)
    else:
        print("Invalid password")
        return None


    


