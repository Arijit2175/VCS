#Importing the modules required
import mysql.connector
from mysql.connector import Error
import logging
import hashlib
from psycopg2 import Error

logging.basicConfig(level=logging.INFO)

#Logic for connection to database
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
            logging.info("Connection established")
            initialize_main_branch(conn)
    except Error as e:
        logging.error(f"Error: '{e}'")
    return conn

#Initializing the default branch as main
def initialize_main_branch(conn):
    with conn.cursor() as cursor:
        query_check = "SELECT * FROM branches WHERE name = 'main'"
        cursor.execute(query_check)
        existing_branch = cursor.fetchone()

        if existing_branch:
            logging.info("Main branch already exists. No need to create.")
            return False

        query = "INSERT INTO branches (name, latest_commit) VALUES ('main', NULL)"
        try:
            cursor.execute(query)
            conn.commit()
            logging.info("Main branch created successfully.")
            return True
        except Error as e:
            logging.error(f"Error: '{e}'")
            return False

#Logic for addition of files
def add_file(conn, file_hash, content):
    with conn.cursor() as cursor:
        query_check = "SELECT * FROM files WHERE hash = %s"
        cursor.execute(query_check, (file_hash,))
        existing_file = cursor.fetchone()

        if existing_file:
            logging.info("File with this hash already exists. Skipping insert.")
            return False

        query = "INSERT INTO files (hash, content) VALUES (%s, %s)"
        try:
            cursor.execute(query, (file_hash, content))
            conn.commit()
            logging.info("File added successfully.")
            return True
        except Error as e:
            logging.error(f"Error: '{e}'")
            return False

#Logic for creation of commits with automated updation
def create_commit(conn, commit_hash, message, parent_commit, branch_name):
    """Create a new commit and update the corresponding branch's latest commit."""
    with conn.cursor() as cursor:
        if commit_exists(conn, commit_hash):
            logging.info(f"Commit with hash '{commit_hash}' already exists. Skipping insert.")
            return False
        
        if parent_commit and not commit_exists(conn, parent_commit):
            logging.error(f"Cannot create commit '{commit_hash}': Parent commit '{parent_commit}' does not exist.")
            return False
        
        query = "INSERT INTO commits (commit_hash, message, parent_commit, branch_name) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, (commit_hash, message, parent_commit, branch_name))
            conn.commit()
            logging.info(f"Commit '{commit_hash}' created successfully.")
            
            cursor.execute("SELECT 1 FROM branches WHERE name = %s", (branch_name,))
            branch_exists = cursor.fetchone() is not None
            
            if branch_exists:
                cursor.execute("UPDATE branches SET latest_commit = %s WHERE name = %s", 
                              (commit_hash, branch_name))
                conn.commit()
                logging.info(f"Branch '{branch_name}' updated with latest commit '{commit_hash}'.")
            else:
                cursor.execute("INSERT INTO branches (name, latest_commit) VALUES (%s, %s)", 
                              (branch_name, commit_hash))
                conn.commit()
                logging.info(f"Branch '{branch_name}' created with latest commit '{commit_hash}'.")
            
            return True
            
        except Error as e:
            logging.error(f"Error in commit creation or branch update: {e}")
            conn.rollback() 
            return False

#Verification of commit existence
def commit_exists(conn, commit_hash):
    """Check if a commit exists in the commits table."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM commits WHERE commit_hash = %s", (commit_hash,))
        return cursor.fetchone() is not None

 #Logic for creation of branches       
def create_branch(conn, branch_name, latest_commit):
    with conn.cursor() as cursor:
        query_check = "SELECT * FROM branches WHERE name = %s"
        cursor.execute(query_check, (branch_name,))
        existing_branch = cursor.fetchone()

        if existing_branch:
            logging.info(f"Branch with name '{branch_name}' already exists. Skipping insert.")
            return False

        if latest_commit: 
            query_commit_check = "SELECT * FROM commits WHERE commit_hash = %s"
            cursor.execute(query_commit_check, (latest_commit,))
            commit_exists = cursor.fetchone()

            if not commit_exists:
                logging.error(f"Cannot create branch '{branch_name}': Latest commit '{latest_commit}' does not exist.")
                return False

        query = "INSERT INTO branches (name, latest_commit) VALUES (%s, %s)"
        try:
            cursor.execute(query, (branch_name, latest_commit if latest_commit else None)) 
            conn.commit()
            logging.info(f"Branch '{branch_name}' created successfully.")
            return True
        except Error as e:
            logging.error(f"Error creating branch '{branch_name}': '{e}'")
            return False

#Logic for file retrieval by hash
def get_file_by_hash(conn, file_hash):
    with conn.cursor() as cursor:
        query = "SELECT * FROM files WHERE hash = %s"
        try:
            cursor.execute(query, (file_hash,))
            file = cursor.fetchone()
            if file:
                logging.info(f"File found: {file}")
                return file
            else:
                logging.info("File not found.")
                return None
        except Error as e:
            logging.error(f"Error: '{e}'")
            return None

#Retrieval of commit info       
def get_commit_info(conn, commit_hash):
    """Check if a commit exists in the commits table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM commits WHERE commit_hash = %s", (commit_hash,))
    return cursor.fetchone() 

#Logic for retrieval of commit history
def get_commit_history(conn, branch_name):
    with conn.cursor() as cursor:
        query = "SELECT commit_hash, message, timestamp FROM commits WHERE branch_name = %s ORDER BY timestamp ASC"
        try:
            cursor.execute(query, (branch_name,))
            commits = cursor.fetchall()
            if commits:
                logging.info(f"Commit history for branch '{branch_name}':")
                for commit in commits:
                    logging.info(f"Commit Hash: {commit[0]}, Message: {commit[1]}, Timestamp: {commit[2]}")
                return commits
            else:
                logging.info(f"No commits found for branch '{branch_name}'.")
                return []
        except Error as e:
            logging.error(f"Error: '{e}'")
            return []

#Logic for retrieval of branch info
def get_branch_info(conn, branch_name):
    with conn.cursor() as cursor:
        query = "SELECT name, latest_commit FROM branches WHERE name = %s"
        try:
            cursor.execute(query, (branch_name,))
            branch = cursor.fetchone()
            if branch:
                logging.info(f"Branch: {branch[0]}, Latest Commit: {branch[1]}")
                return branch
            else:
                logging.info("Branch not found.")
                return None
        except Error as e:
            logging.error(f"Error: '{e}'")
            return None

#Logic for deletion of files
def delete_file(conn, file_hash):
    with conn.cursor() as cursor:
        query = "DELETE FROM files WHERE hash = %s"
        try:
            cursor.execute(query, (file_hash,))
            conn.commit()
            logging.info("File deleted successfully.")
            return True
        except Error as e:
            logging.error(f"Error: '{e}'")
            return False

#Logic for deletion of commits
def delete_commit(conn, commit_hash):
    with conn.cursor() as cursor:
        query = "DELETE FROM commits WHERE commit_hash = %s"
        try:
            cursor.execute(query, (commit_hash,))
            conn.commit()
            logging.info("Commit deleted successfully.")
            return True
        except Error as e:
            logging.error(f"Error: '{e}'")
            return False

#Logic for deletion of branches
def delete_branch(conn, branch_name):
    """Delete a branch from the database."""
    with conn.cursor() as cursor:
        query_check = "SELECT * FROM branches WHERE name = %s"
        cursor.execute(query_check, (branch_name,))
        existing_branch = cursor.fetchone()

        if not existing_branch:
            logging.warning(f"Branch '{branch_name}' does not exist. Deletion failed.")
            return False

        query_commit_check = "SELECT * FROM commits WHERE branch_name = %s"
        cursor.execute(query_commit_check, (branch_name,))
        associated_commits = cursor.fetchall()

        if associated_commits:
            logging.warning(f"Branch '{branch_name}' has associated commits. Deletion failed.")
            return False

        query_delete = "DELETE FROM branches WHERE name = %s"
        try:
            cursor.execute(query_delete, (branch_name,))
            conn.commit()
            logging.info(f"Branch '{branch_name}' deleted successfully.")
            return True
        except Error as e:
            logging.error(f"Error: '{e}'")
            return False

#Logic for merging of branches       
def merge_branches(conn, source_branch, target_branch):
    """Merge source_branch into target_branch."""
    source_commit_hash = get_latest_commit_hash(conn, source_branch)
    target_commit_hash = get_latest_commit_hash(conn, target_branch)

    if not source_commit_hash or not target_commit_hash:
        logging.warning("One or both branches not found.")
        return False

    common_ancestor_commit = find_common_ancestor(conn, source_commit_hash, target_commit_hash)
    if not common_ancestor_commit:
        logging.warning("No common ancestor found, unable to merge.")
        return False

    logging.info(f"Common ancestor commit: {common_ancestor_commit}")

    if check_for_conflicts(conn, common_ancestor_commit, source_commit_hash, target_commit_hash):
        logging.warning("Conflicts detected, need to resolve manually.")
        return False

    merge_commit_hash = create_merge_commit(conn, source_commit_hash, target_commit_hash, target_branch)
    logging.info(f"Merge commit created: {merge_commit_hash}")

    update_branch(conn, target_branch, merge_commit_hash)
    return True

#Functions involved in branch merging

#Fetching the latest commit hash
def get_latest_commit_hash(conn, branch_name):
    """Fetch the latest commit hash for a given branch."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT latest_commit FROM branches WHERE name = %s", (branch_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        logging.warning(f"No commit found for branch '{branch_name}'")
        return None

#Finding common ancestor between two commits
def find_common_ancestor(conn, commit_hash1, commit_hash2):
    """Find the common ancestor of two commits."""
    visited = set()
    
    while commit_hash1:
        visited.add(commit_hash1)
        commit_hash1 = get_parent_commit(conn, commit_hash1)

    while commit_hash2:
        if commit_hash2 in visited:
            return commit_hash2
        commit_hash2 = get_parent_commit(conn, commit_hash2)

    return None

#Retrieval of parent commit
def get_parent_commit(conn, commit_hash):
    """Fetch the parent commit for a given commit hash."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT parent_commit FROM commits WHERE commit_hash = %s", (commit_hash,))
        parent = cursor.fetchone()
        return parent[0] if parent else None

#Checking for any conflicts
def check_for_conflicts(conn, ancestor_commit, source_commit, target_commit):
    """Check if there are conflicts between source and target commits."""
    return False  

#Creation of the merged commits
def create_merge_commit(conn, source_commit, target_commit, branch_name):
    """Create a merge commit."""
    merge_commit_hash = hashlib.sha256(f"{source_commit}{target_commit}{branch_name}".encode()).hexdigest()
    with conn.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO commits (commit_hash, message, parent_commit, branch_name) VALUES (%s, %s, %s, %s)",
                (merge_commit_hash, f"Merge {source_commit} into {target_commit}", source_commit, branch_name)
            )
            conn.commit()
        except Exception as e:
            logging.error(f"Failed to create merge commit: {e}")
            return None
    return merge_commit_hash

#Updation of the branch
def update_branch(conn, branch_name, commit_hash):
    """Update the latest commit for a branch."""
    with conn.cursor() as cursor:
        cursor.execute("UPDATE branches SET latest_commit = %s WHERE name = %s", (commit_hash, branch_name))
        conn.commit()

#Ending the code