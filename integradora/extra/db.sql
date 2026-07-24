-- Active: 1783567323789@@127.0.0.1@3306@integradora

create database integradora

use integradora

create table passwd (
    id int auto_increment,
    passw varchar(255) not null,
    constraint pk primary key (id)
)

create table user (
    id int auto_increment,
    name varchar(20) not null,
    passwd varchar(255) not null,
    username varchar(20) not null,
    date_ date not null,
    email varchar(255) not null,
    role int not null,
    date_kick date,
    strike int not null,
    constraint pk primary key (id)
)

create table message (
    id int auto_increment,
    description text not null,
    date_ date not null,
    del int not null,
    id_user int not null,
    constraint pk primary key (id),
    constraint fk_user_msg foreign key (id_user) references user (id) on delete cascade
)

create table progress (
    id int auto_increment,
    xp int not null,
    accurate float not null,
    id_user int not null,
    constraint pk primary key (id),
    constraint fk_user_pro foreign key (id_user) references user (id) on delete cascade
)

create table premium (
    id int auto_increment,
    payment_method varchar(10) not null,
    amount float not null,
    id_user int not null,
    constraint pk primary key (id),
    constraint fk_user_pre foreign key (id_user) references user (id) on delete cascade
)

create table activity (
    id int auto_increment,
    xp int not null,
    name varchar(20) not null,
    description text not null,
    constraint pk primary key (id)
)

create table result (
    id int auto_increment,
    xp int not null,
    accurate float not null,
    date_ date not null,
    id_user int not null,
    id_activity int not null,
    constraint pk primary key (id),
    constraint fk_user_res foreign key (id_user) references user (id) on delete cascade,
    constraint fk_activity_res foreign key (id_activity) references activity (id)
)

--passwd: NEH.1b.nkg6
insert into user (name, username, passwd, date_, email, role, strike) values
("negatron_griffin", "negatron", "$2b$12$c97mFuugNLr5ogGTZnIstuwMROqILt1bxJtNiNcemL9oOUimaJqQi", '2000-01-01', "admin@nega.com", 9999, 0)