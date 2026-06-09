from modules.db import init_db
from modules.auth import register, login
from modules.vault import add_login_credentials
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
        add_login_credentials(user.id, "netflix", "test", "testest", user.master_key)
    except InvalidCredentials as e:
        print(e)

if __name__ == "__main__":
    main()