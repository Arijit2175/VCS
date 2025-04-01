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

