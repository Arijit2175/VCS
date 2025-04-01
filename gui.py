import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import myvcs 

conn = None

def connect_db():
    """Connect to the MySQL database."""
    global conn
    conn = myvcs.create_connection("localhost", "root", "password", "vcs_db")
    if conn:
        messagebox.showinfo("Success", "Connected to Database")
    else:
        messagebox.showerror("Error", "Failed to Connect")

def add_file_ui():
    """Add a file to the VCS."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    file_hash = simpledialog.askstring("Input", "Enter file hash:")
    content = simpledialog.askstring("Input", "Enter file content:")
    myvcs.add_file(conn, file_hash, content)

def create_commit_ui():
    """Create a commit in the VCS."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    commit_hash = simpledialog.askstring("Input", "Enter commit hash:")
    message = simpledialog.askstring("Input", "Enter commit message:")
    parent_commit = simpledialog.askstring("Input", "Enter parent commit (or leave blank):")
    branch_name = simpledialog.askstring("Input", "Enter branch name:")
    myvcs.create_commit(conn, commit_hash, message, parent_commit or None, branch_name)

def create_branch_ui():
    """Create a new branch."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    branch_name = simpledialog.askstring("Input", "Enter branch name:")
    latest_commit = simpledialog.askstring("Input", "Enter latest commit hash:")
    myvcs.create_branch(conn, branch_name, latest_commit)

def update_branch_ui():
    """Update a branch to a new commit."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    branch_name = simpledialog.askstring("Input", "Enter branch name:")
    latest_commit = simpledialog.askstring("Input", "Enter new latest commit hash:")
    myvcs.update_branch(conn, branch_name, latest_commit)

def get_file_by_hash_ui():
    """Retrieve a file from the VCS by its hash."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    file_hash = simpledialog.askstring("Input", "Enter file hash:")
    myvcs.get_file_by_hash(conn, file_hash)

def get_commit_history():
    branch_name = simpledialog.askstring("Input", "Enter branch name:")
    get_commit_history(conn, branch_name)

def get_branch_info():
    branch_name = simpledialog.askstring("Input", "Enter branch name:")
    get_branch_info(conn, branch_name)

def delete_file():
    file_hash = simpledialog.askstring("Input", "Enter file hash to delete:")
    delete_file(conn, file_hash)

def delete_commit():
    commit_hash = simpledialog.askstring("Input", "Enter commit hash to delete:")
    delete_commit(conn, commit_hash)

def merge_branches():
    source_branch = simpledialog.askstring("Input", "Enter source branch name:")
    target_branch = simpledialog.askstring("Input", "Enter target branch name:")
    merge_branches(conn, source_branch, target_branch)

root = tk.Tk()
root.title("MyVCS GUI")

tk.Button(root, text="Add File", command=add_file).pack(fill=tk.X)
tk.Button(root, text="Create Commit", command=create_commit).pack(fill=tk.X)
tk.Button(root, text="Create Branch", command=create_branch).pack(fill=tk.X)
tk.Button(root, text="Update Branch", command=update_branch).pack(fill=tk.X)
tk.Button(root, text="Get File by Hash", command=get_file_by_hash).pack(fill=tk.X)
tk.Button(root, text="Get Commit History", command=get_commit_history).pack(fill=tk.X)
tk.Button(root, text="Get Branch Info", command=get_branch_info).pack(fill=tk.X)
tk.Button(root, text="Delete File", command=delete_file).pack(fill=tk.X)
tk.Button(root, text="Delete Commit", command=delete_commit).pack(fill=tk.X)
tk.Button(root, text="Merge Branches", command=merge_branches).pack(fill=tk.X)
                                                                    
tk.Button(root, text="Exit", command=root.quit).pack(fill=tk.X)

root.mainloop()