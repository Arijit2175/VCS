create database if not exists myvcs;
use myvcs;

drop table if exists files;
drop table if exists commits;
drop table if exists branches;

create table if not exists files (
    hash varchar(64) primary key,
    content text not null
) ENGINE=InnoDB;

create table if not exists commits (
    id int auto_increment primary key,
    commit_hash varchar(64) unique not null,  
    message text not null,
    timestamp TIMESTAMP default CURRENT_TIMESTAMP,
    parent_commit varchar(64),  
    branch_name varchar(50) not null
) ENGINE=InnoDB;

create table if not exists branches (
    name varchar(50) primary key,
    latest_commit varchar(64)
) ENGINE=InnoDB;

alter table commits
    add constraint fk_commits_parent_commit foreign key (parent_commit) references commits(commit_hash) on delete set null,
    add constraint fk_commits_branch_name foreign key (branch_name) references branches(name) on delete cascade;

ALTER TABLE branches
    ADD CONSTRAINT fk_branches_latest_commit FOREIGN KEY (latest_commit) REFERENCES commits(commit_hash) ON DELETE SET NULL;

CREATE INDEX idx_files_hash ON files(hash);
CREATE INDEX idx_commits_branch_name ON commits(branch_name);