import psycopg2
from psycopg2 import sql


def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="mydb",
            user="postgres",
            password="yaazh",
            host="localhost",
            port="5432"
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