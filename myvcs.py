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

def create_commit(conn, commit_hash, message, parent_commit, branch_name):
    cursor = conn.cursor()
    query = "INSERT INTO commits (commit_hash, message, parent_commit, branch_name) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, (commit_hash, message, parent_commit, branch_name))
        conn.commit()
        print("Commit created successfully.")
    except Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

def create_branch(conn, branch_name, latest_commit):
    cursor = conn.cursor()
    query = "INSERT INTO branches (name, latest_commit) VALUES (%s, %s)"
    try:
        cursor.execute(query, (branch_name, latest_commit))
        conn.commit()
        print("Branch created successfully.")
    except Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

def update_branch(conn, branch_name, latest_commit):
    cursor = conn.cursor()
    query = "UPDATE branches SET latest_commit = %s WHERE name = %s"
    try:
        cursor.execute(query, (latest_commit, branch_name))
        conn.commit()
        print("Branch updated successfully.")
    except Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()

def get_file_by_hash(conn, file_hash):
    cursor = conn.cursor()
    query = "SELECT * FROM files WHERE hash = %s"
    try:
        cursor.execute(query, (file_hash,))
        file = cursor.fetchone()
        if file:
            print(f"File found: {file}")
        else:
            print("File not found.")
    except Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()
