CREATE database if not exists myvcs;
USE myvcs;

create table if not exists files(
    id int auto_increment primary key,
    hash varchar(40) unique not null,
    context text not null
);

create table if not exists commits(
    id int auto_increment primary key,
    commit_hash varchar(40) unique not null,
    message text not null,
    timestamp TIMESTAMP default CURRENT_TIMESTAMP,
    parent_commit varchar(40),
    branch_name varchar(40) not null
);

create table if not exists branches(
    name varchar(50) primary key,
    latest_commit varchar(40)
);