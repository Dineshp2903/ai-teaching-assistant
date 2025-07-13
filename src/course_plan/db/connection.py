import psycopg2
from psycopg2 import sql

# database constants
DB_NAME = "mydb"
DB_USER = "postgres"
DB_PASSWORD = "yaazh"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_db_config():
    """
    Returns the database configuration as a dictionary.
    """
    return {
        "dbname": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT
    }

def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return connection.cursor()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    
def close_db_connection(cursor):
    if cursor:
        cursor.close()
    try:
        connection = cursor.connection
        if connection:
            connection.close()
    except Exception as e:
        print(f"Error closing the database connection: {e}")