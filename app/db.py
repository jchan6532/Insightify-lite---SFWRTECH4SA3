import psycopg2
from app.config import DATABASE_URL


def get_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        raise