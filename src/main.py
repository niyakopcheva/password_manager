from modules.db import init_db
from modules.auth import register, login
from modules.vault import add_login_credentials, get_login_credentials, update_login_credentials
from modules.exceptions import InvalidCredentials
from modules.crypto import decrypt_data


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
        add_login_credentials(user.id, "netflix", "test", "testest", user.master_key)
        
        # Test fetching and decrypting
        saved_creds = get_login_credentials(user.id)
        if saved_creds:
            first_cred = saved_creds[0] # Work with the first credential in the list
            decrypted = decrypt_data(first_cred.encrypted_pass, user.master_key)
            print(f"Fetched Login -> Domain: {first_cred.domain}, Username: {first_cred.associated_username}, Password: {decrypted}")

            update_login_credentials(first_cred.id, first_cred.domain, "testnew", decrypted, user.master_key)
        
    except InvalidCredentials as e:
        print(e)

if __name__ == "__main__":
    main()