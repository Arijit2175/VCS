import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    """Create a database connection to a MySQL database."""
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        if conn.is_connected():
            print("Connection established")
    except Error as e:
        print(f"Error: '{e}'")
    return conn

def add_file(conn, file_hash, content):
    cursor = conn.cursor()
    query = "INSERT INTO files (hash, context) VALUES (%s, %s)"
    try:
        cursor.execute(query, (file_hash, content))
        conn.commit()
        print("File added successfully.")
    except Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()