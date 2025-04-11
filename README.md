# VCS Implementation

## Overview 
This project is a **Version Control System (VCS)** tailored for **MySQL databases**. Inspired by Git, it enables commit tracking, branching, and merging directly in a relational environment. It uses a **Python backend** with **MySQL Connector**, and a **Tkinter GUI frontend** for ease of use.

## Inspiration
This system is inspired by the core principles of **Git**, reimagined through the lens of SQL. Instead of working with file systems and shell commands, the project reimplements Git logic—**commits**, **branches**, **merges**—as a database-backed version control engine. 

It blends **Python**, **MySQL**, and software design to explore how versioning works under the hood, making it a valuable learning project for developers wanting to deepen their understanding of both databases and DevOps tools.

## Features
- Create and manage **branches**  
- Make **commits** with messages and parent tracking  
- **Merge** branches with basic conflict detection  
- Retrieve **commit history**, **file contents**, and **branch info**  
- User-friendly **Tkinter-based GUI**

## Installation
Ensure you have python, MySQL and required packages installed.
Install dependencies with:
```
pip install mysql-connector-python
```

## Process Flow

### 1. **Connection**
On launch, the system connects to the MySQL database using provided credentials and ensures that the `main` branch is initialized.

### 2. **Addition of Files**
Each file is hashed and stored. Duplicate entries are avoided by checking the hash before insertion.

### 3. **Committing Changes**
Each commit includes:
- A unique hash
- Message
- Optional parent commit
- Associated branch

On commit, the `branches` table is updated with the latest commit.

### 4. **Branch Management**
- Create branches pointing to a specific commit
- Update branches as new commits are added

### 5. **Merging**
Performs a fast-forward merge when possible. If no common ancestor is found or branches don't exist, it gracefully handles the error.

### 6. **GUI Interface**
The Tkinter GUI allows users to:
- Input data for commits, branches, retrieval
- View output like commit history and file content
- Get feedback for success or errors in real time

## Applications
This MySQL version control system can be used in a variety of real-world scenarios, including:

- **Database Change Tracking**: Maintain a history of changes in database records, such as configuration files or stored scripts.
- **Educational Tools**: Demonstrate version control concepts (branches, commits, merges) in a simple and visual manner for students learning databases and Git.
- **Lightweight Team Collaboration**: Allow multiple developers to simulate Git-like workflows while working directly with SQL databases.
- **Data Experimentation**: Safely experiment with changes to data or schema, with the ability to revert or merge modifications.
- **Custom DevOps Pipelines**: Integrate with deployment systems to manage different versions of DB content across environments.

## References
You can check these out for easier understanding and further learning:

- **MySQL Python Connector Docs** – https://dev.mysql.com/doc/connector-python/en/  
- **Tkinter GUI Guide** – https://docs.python.org/3/library/tkinter.html  
- **Open-Source Git Internals Book** – https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain   
- **Hashlib in Python (for content hashing)** – https://docs.python.org/3/library/hashlib.html  
- **Software Design Patterns for Versioning Systems** – https://martinfowler.com/bliki/VersionControl.html  
- **Designing Git-like Branching in SQL** – https://github.blog/2020-12-17-commits-are-snapshots-not-diffs/  
- **GitHub Engineering Blog** – https://github.blog/engineering/ 