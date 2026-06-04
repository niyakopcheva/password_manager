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