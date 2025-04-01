CREATE database if not exists myvcs;
USE myvcs;

create table if not exists files(
    id int auto_increment primary key,
    hash varchar(40) unique not null,
    context text not null
);

