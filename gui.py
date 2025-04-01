import tkinter as tk
from tkinter import messagebox, simpledialog
import myvcs  

conn = None  

def connect_db():
    """Connect to MySQL database."""
    global conn
    conn = myvcs.create_connection("localhost", "root", "arijit007", "myvcs")
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
    try:
        myvcs.add_file(conn, file_hash, content)
        messagebox.showinfo("Success", "File added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add file: {e}")

def create_commit_ui():
    """Create a commit in the VCS."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    commit_hash = simpledialog.askstring("Input", "Enter commit hash:")
    message = simpledialog.askstring("Input", "Enter commit message:")
    parent_commit = simpledialog.askstring("Input", "Enter parent commit (or leave blank):")
    branch_name = simpledialog.askstring("Input", "Enter branch name:")
    try:
        myvcs.create_commit(conn, commit_hash, message, parent_commit or None, branch_name)
        messagebox.showinfo("Success", "Commit created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create commit: {e}")

def create_branch_ui():
    """Create a new branch."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    branch_name = simpledialog.askstring("Input", "Enter branch name:")
    latest_commit = simpledialog.askstring("Input", "Enter latest commit hash:")
    try:
        myvcs.create_branch(conn, branch_name, latest_commit)
        messagebox.showinfo("Success", "Branch created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create branch: {e}")

def update_branch_ui():
    """Update a branch to a new commit."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    branch_name = simpledialog.askstring("Input", "Enter branch name:")
    latest_commit = simpledialog.askstring("Input", "Enter new latest commit hash:")
    try:
        myvcs.update_branch(conn, branch_name, latest_commit)
        messagebox.showinfo("Success", "Branch updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update branch: {e}")

def get_file_by_hash_ui():
    """Retrieve a file from the VCS by its hash and show the content in a messagebox."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    file_hash = simpledialog.askstring("Input", "Enter file hash:")
    try:
        content = myvcs.get_file_by_hash(conn, file_hash)
        if content:
            messagebox.showinfo("File Content", f"Content: {content}")
        else:
            messagebox.showerror("Error", "File not found")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve file: {e}")

def get_commit_history_ui():
    """Get commit history of a branch."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    branch_name = simpledialog.askstring("Input", "Enter branch name:")
    try:
        history = myvcs.get_commit_history(conn, branch_name)
        messagebox.showinfo("Commit History", "\n".join(history) if history else "No commits found")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get commit history: {e}")

def get_branch_info_ui():
    """Get details about a branch."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    branch_name = simpledialog.askstring("Input", "Enter branch name:")
    try:
        info = myvcs.get_branch_info(conn, branch_name)
        messagebox.showinfo("Branch Info", str(info) if info else "No branch found")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get branch info: {e}")

def delete_file_ui():
    """Delete a file from the VCS."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    file_hash = simpledialog.askstring("Input", "Enter file hash to delete:")
    try:
        myvcs.delete_file(conn, file_hash)
        messagebox.showinfo("Success", "File deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete file: {e}")

def delete_commit_ui():
    """Delete a commit from the VCS."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    commit_hash = simpledialog.askstring("Input", "Enter commit hash to delete:")
    try:
        myvcs.delete_commit(conn, commit_hash)
        messagebox.showinfo("Success", "Commit deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete commit: {e}")

def merge_branches_ui():
    """Merge two branches in the VCS."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    source_branch = simpledialog.askstring("Input", "Enter source branch name:")
    target_branch = simpledialog.askstring("Input", "Enter target branch name:")
    try:
        myvcs.merge_branches(conn, source_branch, target_branch)
        messagebox.showinfo("Success", "Branches merged successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to merge branches: {e}")

def close_app():
    """Close the application."""
    if conn:
        conn.close()
    root.quit()

root = tk.Tk()
root.title("MyVCS GUI")
root.geometry("400x500")
root.resizable(True, True)

frame = tk.Frame(root, padx=20, pady=10)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

tk.Button(frame, text="Connect to Database", command=connect_db).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Add File", command=add_file_ui).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Create Commit", command=create_commit_ui).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Create Branch", command=create_branch_ui).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Update Branch", command=update_branch_ui).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Get File by Hash", command=get_file_by_hash_ui).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Get Commit History", command=get_commit_history_ui).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Get Branch Info", command=get_branch_info_ui).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Delete File", command=delete_file_ui).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Delete Commit", command=delete_commit_ui).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Merge Branches", command=merge_branches_ui).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Exit", command=close_app).pack(fill=tk.X, pady=5)

root.mainloop()