import tkinter as tk
from tkinter import messagebox
from myvcs import create_connection, add_file, create_commit, create_branch, update_branch, get_file_by_hash, get_commit_history, get_branch_info, delete_file, delete_commit, merge_branches

def connect_db():
    global conn
    conn = create_connection("localhost", "root", "password", "vcs_db")
    if conn:
        messagebox.showinfo("Success", "Connected to Database")
    else:
        messagebox.showerror("Error", "Failed to Connect")

def add_file_ui():
    file_hash = file_hash_entry.get()
    content = content_entry.get()
    add_file(conn, file_hash, content)

def create_commit_ui():
    commit_hash = commit_hash_entry.get()
    message = commit_message_entry.get()
    parent_commit = parent_commit_entry.get() or None
    branch_name = commit_branch_entry.get()
    create_commit(conn, commit_hash, message, parent_commit, branch_name)

def create_branch():
    branch_name = simpledialog.askstring("Input", "Enter branch name:")
    latest_commit = simpledialog.askstring("Input", "Enter latest commit hash:")
    create_branch(conn, branch_name, latest_commit)

def update_branch():
    branch_name = simpledialog.askstring("Input", "Enter branch name:")
    latest_commit = simpledialog.askstring("Input", "Enter new latest commit hash:")
    update_branch(conn, branch_name, latest_commit)

def get_file_by_hash():
    file_hash = simpledialog.askstring("Input", "Enter file hash:")
    get_file_by_hash(conn, file_hash)

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