CREATE DATABASE IF NOT EXISTS myvcs;
USE myvcs;

CREATE TABLE IF NOT EXISTS branches (
    name VARCHAR(50) PRIMARY KEY,
    latest_commit VARCHAR(64)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS commits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commit_hash VARCHAR(64) UNIQUE NOT NULL,  
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parent_commit VARCHAR(64),  
    branch_name VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

ALTER TABLE branches
ADD FOREIGN KEY (latest_commit) REFERENCES commits(commit_hash) ON DELETE SET NULL;

ALTER TABLE commits
ADD FOREIGN KEY (parent_commit) REFERENCES commits(commit_hash) ON DELETE SET NULL,
ADD FOREIGN KEY (branch_name) REFERENCES branches(name) ON DELETE CASCADE;

CREATE INDEX idx_files_hash ON files(hash);
CREATE INDEX idx_commits_branch_name ON commits(branch_name);