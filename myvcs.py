import mysql.connector
from mysql.connector import Error
import logging
import hashlib

logging.basicConfig(level=logging.INFO)

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

def create_commit(conn, commit_hash, message, parent_commit, branch_name):
    with conn.cursor() as cursor:
        query_check = "SELECT * FROM commits WHERE commit_hash = %s"
        cursor.execute(query_check, (commit_hash,))
        existing_commit = cursor.fetchone()

        if existing_commit:
            logging.info(f"Commit with hash {commit_hash} already exists. Skipping insert.")
            return False

        query = "INSERT INTO commits (commit_hash, message, parent_commit, branch_name) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(query, (commit_hash, message, parent_commit, branch_name))
            conn.commit()
            logging.info("Commit created successfully.")
            return True
        except Error as e:
            logging.error(f"Error: '{e}'")
            return False
        
def create_branch(conn, branch_name, latest_commit):
    with conn.cursor() as cursor:
        query_check = "SELECT * FROM branches WHERE name = %s"
        cursor.execute(query_check, (branch_name,))
        existing_branch = cursor.fetchone()

        if existing_branch:
            logging.info(f"Branch with name '{branch_name}' already exists. Skipping insert.")
            return False

        if latest_commit is not None and latest_commit != "":
            query_commit_check = "SELECT * FROM commits WHERE commit_hash = %s"
            cursor.execute(query_commit_check, (latest_commit,))
            commit_exists = cursor.fetchone()

            if not commit_exists:
                logging.error(f"Cannot create branch '{branch_name}': Latest commit '{latest_commit}' does not exist.")
                return False

        query = "INSERT INTO branches (name, latest_commit) VALUES (%s, %s)"
        try:
            cursor.execute(query, (branch_name, latest_commit))
            conn.commit()
            logging.info("Branch created successfully.")
            return True
        except Error as e:
            logging.error(f"Error: '{e}'")
            return False

def update_branch(conn, branch_name, latest_commit):
    with conn.cursor() as cursor:
        query_check_branch = "SELECT * FROM branches WHERE name = %s"
        cursor.execute(query_check_branch, (branch_name,))
        existing_branch = cursor.fetchone()

        if existing_branch:
            query_check_commit = "SELECT * FROM commits WHERE commit_hash = %s"
            cursor.execute(query_check_commit, (latest_commit,))
            commit_exists = cursor.fetchone()

            if commit_exists:
                query_update = "UPDATE branches SET latest_commit = %s WHERE name = %s"
                try:
                    cursor.execute(query_update, (latest_commit, branch_name))
                    conn.commit()
                    logging.info("Branch updated successfully.")
                    return True
                except Error as e:
                    logging.error(f"Error: '{e}'")
                    return False
            else:
                logging.warning(f"Commit '{latest_commit}' does not exist. Update failed.")
                return False
        else:
            logging.warning(f"Branch '{branch_name}' does not exist. Update failed.")
            return False

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
        
def get_commit_info(conn, commit_hash):
    """Check if a commit exists in the commits table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM commits WHERE commit_hash = %s", (commit_hash,))
    return cursor.fetchone() 

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

def delete_branch(conn, branch_name):
def merge_branches(conn, source_branch, target_branch):
    with conn.cursor() as cursor:
        query = "SELECT latest_commit FROM branches WHERE name = %s"
        cursor.execute(query, (source_branch,))
        source_commit = cursor.fetchone()
        cursor.execute(query, (target_branch,))
        target_commit = cursor.fetchone()

        if not source_commit or not target_commit:
            logging.warning("One or both branches not found.")
            return False

        source_commit_hash = source_commit[0]
        target_commit_hash = target_commit[0]

        common_ancestor_commit = find_common_ancestor(conn, source_commit_hash, target_commit_hash)

        if not common_ancestor_commit:
            logging.warning("No common ancestor found, unable to merge.")
            return False

        logging.info(f"Common ancestor commit: {common_ancestor_commit}")

        conflicts = check_for_conflicts(conn, common_ancestor_commit, source_commit_hash, target_commit_hash)
        
        if conflicts:
            logging.warning("Conflicts detected, need to resolve manually.")
            return False
        
        merge_commit_hash = create_merge_commit(conn, source_commit_hash, target_commit_hash, target_branch)
        logging.info(f"Merge commit created: {merge_commit_hash}")

        update_branch(conn, target_branch, merge_commit_hash)
        
        return True

def find_common_ancestor(conn, commit_hash1, commit_hash2):
    """Find the common ancestor of two commits"""
    with conn.cursor() as cursor:
        query = "SELECT parent_commit FROM commits WHERE commit_hash = %s"
        
        parents1 = [commit_hash1]
        parents2 = [commit_hash2]
        
        while parents1 or parents2:
            if parents1:
                cursor.execute(query, (parents1.pop(),))
                parent1 = cursor.fetchone()
                if parent1:
                    parents1.append(parent1[0])

            if parents2:
                cursor.execute(query, (parents2.pop(),))
                parent2 = cursor.fetchone()
                if parent2:
                    parents2.append(parent2[0])

            common_ancestors = set(parents1) & set(parents2)
            if common_ancestors:
                return common_ancestors.pop()  

    return None

def check_for_conflicts(conn, ancestor_commit, source_commit, target_commit):
    """Check if there are conflicts between source and target commits"""
    return False

def create_merge_commit(conn, source_commit, target_commit, branch_name):
    """Create a merge commit"""
    merge_commit_hash = hashlib.sha256(f"{source_commit}{target_commit}{branch_name}".encode()).hexdigest()
    query = "INSERT INTO commits (commit_hash, message, parent_commit, branch_name) VALUES (%s, %s, %s, %s)"
    with conn.cursor() as cursor:
        cursor.execute(query, (merge_commit_hash, f"Merge {source_commit} into {target_commit}", source_commit, branch_name))
        conn.commit()
    return merge_commit_hash