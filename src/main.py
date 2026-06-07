from modules.db import init_db
from modules.auth import register, login

def main():
    print("Starting Password Manager...")
    init_db()
    print("Application is ready.")
    # register("testUser", "testpass")
    # login("testUser", "testpass")     # prints Access granted!
    # login("userNotExist", "testpass") # prints User not found!
    login("testUser", "wrongpass")      # prints Invalid password

if __name__ == "__main__":
    main()