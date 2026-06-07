import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    

def init_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor() 

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    master_pass_hash VARCHAR(255) NOT NULL,
                    login_salt BYTEA NOT NULL,
                    vault_salt BYTEA NOT NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                    id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(id) ON DELETE CASCADE,
                    domain VARCHAR(255) NOT NULL,
                    associated_username VARCHAR(255) NOT NULL,
                    encrypted_pass BYTEA NOT NULL
                );
            """)

            conn.commit()
            print("Db tables initialized successfully/already exist.")

        except Exception as e:
            print(f"Error initializing tables: {e}")
            
        finally:
            cursor.close()
            conn.close()