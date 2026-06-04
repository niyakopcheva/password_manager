from modules.db import get_db_connection

def main():
    conn = get_db_connection()
    if conn:
        print("Successfully connected to database!")
        conn.close()

if __name__ == "__main__":
    main()