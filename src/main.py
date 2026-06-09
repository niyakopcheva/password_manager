from modules.db import init_db
from modules.auth import register, login
from modules.vault import add_login_credentials, get_login_credentials, decrypt_password
from modules.exceptions import InvalidCredentials

def main():
    print("Starting Password Manager...")
    init_db()
    print("Application is ready.")
    try:
        # register("testUser", "testpass")
        username="testUser"
        passw="testpass"
        user =login(username, passw)     # prints Access granted!
        # login("userNotExist", "testpass") # prints User not found!
        # login("testUser", "wrongpass")      # prints Invalid password
        # add_login_credentials(user.id, "netflix", "test", "testest", user.master_key)
        
        # Test fetching and decrypting
        saved_cred = get_login_credentials(user.id)
        if saved_cred:
            decrypted = decrypt_password(saved_cred.encrypted_pass, user.master_key)
            print(f"Fetched Login -> Domain: {saved_cred.domain}, Username: {saved_cred.associated_username}, Password: {decrypted}")
    except InvalidCredentials as e:
        print(e)

if __name__ == "__main__":
    main()