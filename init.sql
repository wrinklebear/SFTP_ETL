create database test;
use test;
create table user
(
id int auto_increment primary key,
username varchar(64) unique not null,
email varchar(120) unique not null,
password_hash varchar(128) not null,
avatar varchar(128) not null
);
insert into user values(1, "aaocking","1269357664@qq.com","648451kobe","avaterpath");
