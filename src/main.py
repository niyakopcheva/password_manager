from modules.db import init_db

def main():
    print("Starting Password Manager...")
    init_db()
    print("Application is ready.")

if __name__ == "__main__":
    main()