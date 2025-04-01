CREATE DATABASE IF NOT EXISTS myvcs;
USE myvcs;

CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hash VARCHAR(40) UNIQUE NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS commits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commit_hash VARCHAR(40) UNIQUE NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parent_commit VARCHAR(40),
    branch_name VARCHAR(50) NOT NULL,  
    FOREIGN KEY (parent_commit) REFERENCES commits(commit_hash) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS branches (
    name VARCHAR(50) PRIMARY KEY,
    latest_commit VARCHAR(40),
    FOREIGN KEY (latest_commit) REFERENCES commits(commit_hash) ON DELETE SET NULL
);

CREATE INDEX idx_files_hash ON files(hash);
CREATE INDEX idx_commits_branch_name ON commits(branch_name);
