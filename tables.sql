create database if not exists myvcs;
use myvcs;

DROP TABLE IF EXISTS files;
DROP TABLE IF EXISTS commits;
DROP TABLE IF EXISTS branches;

CREATE TABLE IF NOT EXISTS files (
    hash VARCHAR(64) PRIMARY KEY,
    content TEXT NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS commits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commit_hash VARCHAR(64) UNIQUE NOT NULL,  
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parent_commit VARCHAR(64),  
    branch_name VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS branches (
    name VARCHAR(50) PRIMARY KEY,
    latest_commit VARCHAR(64)
) ENGINE=InnoDB;

ALTER TABLE commits
    ADD CONSTRAINT fk_commits_parent_commit FOREIGN KEY (parent_commit) REFERENCES commits(commit_hash) ON DELETE SET NULL,
    ADD CONSTRAINT fk_commits_branch_name FOREIGN KEY (branch_name) REFERENCES branches(name) ON DELETE CASCADE;

ALTER TABLE branches
    ADD CONSTRAINT fk_branches_latest_commit FOREIGN KEY (latest_commit) REFERENCES commits(commit_hash) ON DELETE SET NULL;

CREATE INDEX idx_files_hash ON files(hash);
CREATE INDEX idx_commits_branch_name ON commits(branch_name);