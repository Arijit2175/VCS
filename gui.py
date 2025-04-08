import tkinter as tk
from tkinter import messagebox, simpledialog
import myvcs  
import re

conn = None  

def connect_db():
    """Connect to MySQL database."""
    global conn

    input_window = tk.Toplevel(root)
    input_window.title("Database Connection")
    input_window.geometry("300x220")  

    tk.Label(input_window, text="Enter database name:").pack(pady=5)
    db_name_entry = tk.Entry(input_window, width=30)  
    db_name_entry.pack(pady=5)

    tk.Label(input_window, text="Enter database password:").pack(pady=5)
    db_password_entry = tk.Entry(input_window, show='*', width=30)  
    db_password_entry.pack(pady=5)

    def on_connect():
        """Handle the connection when the button is pressed."""
        global conn
        db_name = db_name_entry.get()
        db_password = db_password_entry.get()

        if not db_name:
            messagebox.showerror("Error", "Database name cannot be empty.")
            return
        
        conn = myvcs.create_connection("localhost", "root", db_password, db_name)
        if conn:
            messagebox.showinfo("Success", "Connected to Database")
            input_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to Connect")

    connect_button = tk.Button(input_window, text="Connect", command=on_connect)
    connect_button.pack(pady=10)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.pack(pady=5)

def add_file_ui():
    """Add a file to the VCS."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return
    
    input_window = tk.Toplevel(root)
    input_window.title("Add File")
    input_window.geometry("300x290")

    tk.Label(input_window, text="Enter file hash:").pack(pady=5)
    file_hash_entry = tk.Entry(input_window, width=30) 
    file_hash_entry.pack(pady=5)

    tk.Label(input_window, text="Enter file content:").pack(pady=5)
    content_entry = tk.Text(input_window, width=30, height=5)  
    content_entry.pack(pady=5)

    def on_add_file():
        """Handle the addition of the file when the button is pressed."""
        file_hash = file_hash_entry.get()
        content = content_entry.get("1.0", tk.END).strip()

        if not file_hash or not content:
            messagebox.showerror("Error", "File hash and content cannot be empty.")
            return

        try:
            success = myvcs.add_file(conn, file_hash, content)
            if success:
                messagebox.showinfo("Success", "File added successfully!")
                input_window.destroy() 
            else:
                messagebox.showerror("Error", "File with this hash already exists.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add file: {e}")
    
    add_button = tk.Button(input_window, text="Add File", command=on_add_file)
    add_button.pack(pady=10)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.pack(pady=5)

def create_commit_ui():
    """Create a commit in the VCS."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    input_window = tk.Toplevel(root)
    input_window.title("Create Commit")
    input_window.geometry("400x450")  

    tk.Label(input_window, text="Enter commit hash:").pack(pady=5)
    commit_hash_entry = tk.Entry(input_window, width=40)  
    commit_hash_entry.pack(pady=5)

    tk.Label(input_window, text="Enter commit message:").pack(pady=5)
    message_entry = tk.Text(input_window, width=40, height=5)  
    message_entry.pack(pady=5)

    tk.Label(input_window, text="Enter parent commit (or leave blank):").pack(pady=5)
    parent_commit_entry = tk.Entry(input_window, width=40)  
    parent_commit_entry.pack(pady=5)

    tk.Label(input_window, text="Enter branch name:").pack(pady=5)
    branch_name_entry = tk.Entry(input_window, width=40)  
    branch_name_entry.pack(pady=5)
    
    def on_create_commit():
        """Handle the creation of the commit when the button is pressed."""
        commit_hash = commit_hash_entry.get()
        message = message_entry.get("1.0", tk.END).strip()  
        parent_commit = parent_commit_entry.get()
        branch_name = branch_name_entry.get()

        if not commit_hash or not message or not branch_name:
            messagebox.showerror("Error", "Commit hash, message, and branch name cannot be empty.")
            return

        branch_info = myvcs.get_branch_info(conn, branch_name)
        if not branch_info:
            messagebox.showerror("Error", f"Branch '{branch_name}' does not exist.")
            return

        try:
            success = myvcs.create_commit(conn, commit_hash, message, parent_commit or None, branch_name)
            if success:
                messagebox.showinfo("Success", "Commit created successfully!")
                input_window.destroy()  
            else:
                messagebox.showerror("Error", "Commit with this hash already exists.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create commit: {e}")

    create_button = tk.Button(input_window, text="Create Commit", command=on_create_commit)
    create_button.pack(pady=10)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.pack(pady=5)

def create_branch_ui():
    """Create a new branch."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    input_window = tk.Toplevel(root)
    input_window.title("Create Branch")
    input_window.geometry("400x250")  

    tk.Label(input_window, text="Enter branch name:").pack(pady=5)
    branch_name_entry = tk.Entry(input_window, width=40)  
    branch_name_entry.pack(pady=5)

    tk.Label(input_window, text="Enter latest commit hash (or leave blank):").pack(pady=5)
    latest_commit_entry = tk.Entry(input_window, width=40)  
    latest_commit_entry.pack(pady=5)
    
    def on_create_branch():
        """Handle the creation of the branch when the button is pressed."""
        branch_name = branch_name_entry.get()
        latest_commit = latest_commit_entry.get().strip() 

        if not branch_name:
            messagebox.showerror("Error", "Branch name cannot be empty.")
            return

        existing_branch_info = myvcs.get_branch_info(conn, branch_name)
        if existing_branch_info:
            messagebox.showerror("Error", f"Branch '{branch_name}' already exists.")
            return

        if latest_commit:
            commit_info = myvcs.get_commit_info(conn, latest_commit)  
            if not commit_info:
                messagebox.showerror("Error", f"Latest commit '{latest_commit}' does not exist.")
                return

        try:
            success = myvcs.create_branch(conn, branch_name, latest_commit)
            if success:
                messagebox.showinfo("Success", "Branch created successfully!")
                input_window.destroy()  
            else:
                messagebox.showerror("Error", "Failed to create branch.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create branch: {e}")

    create_button = tk.Button(input_window, text="Create Branch", command=on_create_branch)
    create_button.pack(pady=10)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.pack(pady=5)

def update_branch_ui():
    """Update a branch to a new commit."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return
    
    input_window = tk.Toplevel(root)
    input_window.title("Update Branch")
    input_window.geometry("400x250")  

    tk.Label(input_window, text="Enter branch name:").pack(pady=5)
    branch_name_entry = tk.Entry(input_window, width=40)  
    branch_name_entry.pack(pady=5)

    tk.Label(input_window, text="Enter new latest commit hash:").pack(pady=5)
    latest_commit_entry = tk.Entry(input_window, width=40)  
    latest_commit_entry.pack(pady=5)
 
    def on_update_branch():
        """Handle the update of the branch when the button is pressed."""
        branch_name = branch_name_entry.get().strip()
        latest_commit = latest_commit_entry.get().strip()

        if not branch_name or not latest_commit:
            messagebox.showerror("Error", "Branch name and latest commit cannot be empty.")
            return

        commit_info = myvcs.get_commit_info(conn, latest_commit)  
        if not commit_info:
            messagebox.showerror("Error", f"Latest commit '{latest_commit}' does not exist.")
            return

        try:
            success = myvcs.update_branch(conn, branch_name, latest_commit)
            if success:
                messagebox.showinfo("Success", "Branch updated successfully!")
                input_window.destroy()  
            else:
                messagebox.showerror("Error", "Branch not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update branch: {e}")

    update_button = tk.Button(input_window, text="Update Branch", command=on_update_branch)
    update_button.pack(pady=10)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.pack(pady=5)

def get_file_by_hash_ui():
    """Retrieve a file from the VCS by its hash and display it in a new window."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    input_window = tk.Toplevel(root)
    input_window.title("Retrieve File by Hash")
    input_window.geometry("400x150") 

    tk.Label(input_window, text="Enter file hash:").pack(pady=5)
    file_hash_entry = tk.Entry(input_window, width=40) 
    file_hash_entry.pack(pady=5)

    def on_retrieve_file():
        """Handle the retrieval of the file when the button is pressed."""
        file_hash = file_hash_entry.get().strip()
        if not file_hash:
            messagebox.showerror("Error", "File hash cannot be empty.")
            return

        try:
            content = myvcs.get_file_by_hash(conn, file_hash)
            if content:
                file_content = content[1]  

                file_window = tk.Toplevel(root)
                file_window.title(f"File Content: {file_hash}")
                file_window.geometry("600x400")  
                
                text_widget = tk.Text(file_window, wrap=tk.WORD)
                text_widget.insert(tk.END, file_content)  
                text_widget.pack(expand=True, fill=tk.BOTH)

                text_widget.config(state=tk.DISABLED)  
            else:
                messagebox.showerror("Error", "File not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve file: {e}")

    retrieve_button = tk.Button(input_window, text="Retrieve File", command=on_retrieve_file)
    retrieve_button.pack(pady=10)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.pack(pady=5)

def get_commit_history_ui():
    """Get commit history of a branch and display it in a pop-up window."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    input_window = tk.Toplevel(root)
    input_window.title("Get Commit History")
    input_window.geometry("400x150")  

    tk.Label(input_window, text="Enter branch name:").pack(pady=5)
    branch_name_entry = tk.Entry(input_window, width=40)  
    branch_name_entry.pack(pady=5)

    def on_get_commit_history():
        """Handle the retrieval of commit history when the button is pressed."""
        branch_name = branch_name_entry.get().strip()
        if not branch_name:
            messagebox.showerror("Error", "Branch name cannot be empty.")
            return

        try:
            history = myvcs.get_commit_history(conn, branch_name)
            if history:
                history_str = "\n".join(f"Commit Hash: {commit[0]}, Message: {commit[1]}, Timestamp: {commit[2]}" for commit in history)

                history_window = tk.Toplevel(root)
                history_window.title(f"Commit History: {branch_name}")
                history_window.geometry("600x400") 
                
                text_widget = tk.Text(history_window, wrap=tk.WORD)
                text_widget.insert(tk.END, history_str)
                text_widget.pack(expand=True, fill=tk.BOTH)

                text_widget.config(state=tk.DISABLED)
            else:
                messagebox.showinfo("Commit History", "No commits found for this branch")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get commit history: {e}")

    get_history_button = tk.Button(input_window, text="Get Commit History", command=on_get_commit_history)
    get_history_button.pack(pady=10)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.pack(pady=5)

def get_branch_info_ui():
    """Get details about a branch and display it in a pop-up window."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    input_window = tk.Toplevel(root)
    input_window.title("Get Branch Info")
    input_window.geometry("400x150") 

    tk.Label(input_window, text="Enter branch name:").pack(pady=5)
    branch_name_entry = tk.Entry(input_window, width=40)  
    branch_name_entry.pack(pady=5)

    def on_get_branch_info():
        """Handle the retrieval of branch info when the button is pressed."""
        branch_name = branch_name_entry.get().strip()
        if not branch_name:
            messagebox.showerror("Error", "Branch name cannot be empty.")
            return

        try:
            info = myvcs.get_branch_info(conn, branch_name)
            if info:
                info_str = f"Branch Name: {info[0]}\nLatest Commit: {info[1]}"

                info_window = tk.Toplevel(root)
                info_window.title(f"Branch Info: {branch_name}")
                info_window.geometry("500x300") 

                text_widget = tk.Text(info_window, wrap=tk.WORD)
                text_widget.insert(tk.END, info_str)
                text_widget.pack(expand=True, fill=tk.BOTH)

                text_widget.config(state=tk.DISABLED)
            else:
                messagebox.showinfo("Branch Info", "No branch found with that name")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get branch info: {e}")

    get_info_button = tk.Button(input_window, text="Get Branch Info", command=on_get_branch_info)
    get_info_button.pack(pady=10)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.pack(pady=5)

def delete_file_ui():
    """Delete a file from the VCS."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    input_window = tk.Toplevel(root)
    input_window.title("Delete File")
    input_window.geometry("400x150") 

    tk.Label(input_window, text="Enter file hash to delete:").pack(pady=5)
    file_hash_entry = tk.Entry(input_window, width=40) 
    file_hash_entry.pack(pady=5)

    def on_delete_file():
        """Handle the deletion of the file when the button is pressed."""
        file_hash = file_hash_entry.get().strip()
        if not file_hash:
            messagebox.showerror("Error", "File hash cannot be empty.")
            return

        try:
            success = myvcs.delete_file(conn, file_hash)
            if success:
                messagebox.showinfo("Success", "File deleted successfully!")
                input_window.destroy() 
            else:
                messagebox.showerror("Error", "File not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete file: {e}")

    delete_button = tk.Button(input_window, text="Delete File", command=on_delete_file)
    delete_button.pack(pady=10)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.pack(pady=5)

def delete_commit_ui():
    """Delete a commit from the VCS."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    input_window = tk.Toplevel(root)
    input_window.title("Delete Commit")
    input_window.geometry("400x150") 

    tk.Label(input_window, text="Enter commit hash to delete:").pack(pady=5)
    commit_hash_entry = tk.Entry(input_window, width=40) 
    commit_hash_entry.pack(pady=5)

    def on_delete_commit():
        """Handle the deletion of the commit when the button is pressed."""
        commit_hash = commit_hash_entry.get().strip()
        if not commit_hash:
            messagebox.showerror("Error", "Commit hash cannot be empty.")
            return

        try:
            success = myvcs.delete_commit(conn, commit_hash)
            if success:
                messagebox.showinfo("Success", "Commit deleted successfully!")
                input_window.destroy()
            else:
                messagebox.showerror("Error", "Commit not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete commit: {e}")

    delete_button = tk.Button(input_window, text="Delete Commit", command=on_delete_commit)
    delete_button.pack(pady=10)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.pack(pady=5)

def delete_branch_ui():
    """Delete a branch from the VCS."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    input_window = tk.Toplevel(root)
    input_window.title("Delete Branch")
    input_window.geometry("400x150")  

    tk.Label(input_window, text="Enter branch name to delete:").pack(pady=5)
    branch_name_entry = tk.Entry(input_window, width=40) 
    branch_name_entry.pack(pady=5)

    def on_delete_branch():
        """Handle the deletion of the branch when the button is pressed."""
        branch_name = branch_name_entry.get().strip()
        if not branch_name:
            messagebox.showerror("Error", "Branch name cannot be empty.")
            return

        try:
            success = myvcs.delete_branch(conn, branch_name)
            if success:
                messagebox.showinfo("Success", f"Branch '{branch_name}' deleted successfully!")
                input_window.destroy()  
            else:
                messagebox.showerror("Error", f"Branch '{branch_name}' not found or has associated commits.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete branch: {e}")

    delete_button = tk.Button(input_window, text="Delete Branch", command=on_delete_branch)
    delete_button.pack(pady=10)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.pack(pady=5)

def merge_branches_ui():
    """Merge two branches in the VCS after validating their existence."""
    if conn is None:
        messagebox.showerror("Error", "No database connection")
        return

    input_window = tk.Toplevel(root)
    input_window.title("Merge Branches")
    input_window.geometry("400x200")  

    tk.Label(input_window, text="Enter source branch name:").pack(pady=5)
    source_branch_entry = tk.Entry(input_window, width=40) 
    source_branch_entry.pack(pady=5)

    tk.Label(input_window, text="Enter target branch name:").pack(pady=5)
    target_branch_entry = tk.Entry(input_window, width=40) 
    target_branch_entry.pack(pady=5)

    def on_merge_branches():
        """Handle the merging of branches when the button is pressed."""
        source_branch = source_branch_entry.get().strip()
        target_branch = target_branch_entry.get().strip()

        if not source_branch or not target_branch:
            messagebox.showerror("Error", "Both source and target branch names cannot be empty.")
            return

        if not source_branch.isidentifier() or not target_branch.isidentifier():
            messagebox.showerror("Error", "Branch names must be valid identifiers.")
            return

        try:
            source_info = myvcs.get_branch_info(conn, source_branch)
            target_info = myvcs.get_branch_info(conn, target_branch)

            if not source_info:
                messagebox.showerror("Error", f"Source branch '{source_branch}' not found")
                return

            if not target_info:
                messagebox.showerror("Error", f"Target branch '{target_branch}' not found")
                return

            merge_success = myvcs.merge_branches(conn, source_branch, target_branch)

            if merge_success:
                messagebox.showinfo("Success", "Branches merged successfully!")
                source_branch_entry.delete(0, tk.END)  
                target_branch_entry.delete(0, tk.END)  
            else:
                messagebox.showwarning("Warning", "Merge resulted in conflicts. Please resolve them manually.")

            input_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge branches: {str(e)}")

    merge_button = tk.Button(input_window, text="Merge Branches", command=on_merge_branches)
    merge_button.pack(pady=10)

    cancel_button = tk.Button(input_window, text="Cancel", command=input_window.destroy)
    cancel_button.pack(pady=5)

def close_app():
    """Close the application."""
    if conn:
        conn.close()
    root.quit()

root = tk.Tk()
root.title("MyVCS GUI")
root.geometry("400x530")
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
tk.Button(frame, text="Delete Branch", command=delete_branch_ui).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Merge Branches", command=merge_branches_ui).pack(fill=tk.X, pady=5)
tk.Button(frame, text="Exit", command=close_app).pack(fill=tk.X, pady=5)

root.mainloop()