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
    constraint pk primary key (id)
)

create table message (
    id int auto_increment,
    description text not null,
    date_ date not null,
    id_user int not null,
    constraint pk primary key (id),
    constraint fk_user_msg foreign key (id_user) references user (id)
)

create table progress (
    id int auto_increment,
    xp int not null,
    accurate float not null,
    improvement float not null,
    id_user int not null,
    constraint pk primary key (id),
    constraint fk_user_pro foreign key (id_user) references user (id)
)

create table premium (
    id int auto_increment,
    payment_method varchar(10) not null,
    amount float not null,
    id_user int not null,
    constraint pk primary key (id),
    constraint fk_user_pre foreign key (id_user) references user (id)
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
    improvement float not null,
    date_ date not null,
    id_user int not null,
    id_activity int not null,
    constraint pk primary key (id),
    constraint fk_user_res foreign key (id_user) references user (id),
    constraint fk_activity_res foreign key (id_activity) references activity (id)
)

insert into user (name, username, passwd, date_, email, role) values
("Juan", "xXJuanProXx", "nosenose", '2006-01-01', "juan@juan.com", 1),
("Yo", "yo999", "ibdfkhji", '2006-01-01', "yo@juan.com", 1),
("antonimus", "anonimus", "jobhvugv", '2006-01-01', "juan@yo.com", 1),
("mclovin", "yo_", "qwermnb", '2006-01-01', "mclovin@xdddd.com", 1),
("mclovin", "denmedebaja", "xdxdxdxdxd", '2006-01-01', "xd@xdddd.com", 1);

select * from user

insert into progress (xp, accurate, improvement, id_user) values
(999, 97.3, 4.07, 1),
(123, 56.7, 2.5, 2),
(324, 78.9, 3.9, 3),
(1098, 89.4, 7.3, 4),
(879, 77.34, 4.1, 5)

insert into premium (payment_method, amount, id_user) values
(1, 5.4, 3),
(2, 6, 4);

insert into result (xp, accurate, improvement, date_, id_user, id_activity) values
(23, 62.5, 2.1, '2006-01-01', 2, 1),
(21, 42.8, 2, '2006-01-01', 2, 3),
(30, 35.6, 3.2, '2006-01-01', 1, 4),
(16, 45.3, 4.1, '2006-01-01', 1, 2),
(29, 56.2, 6.5, '2006-01-01', 3, 5),
(52, 78.4, 8.3, '2006-01-01', 3, 4);

insert into activity (xp, name, description) values
(50, "Actividad 1", "No sé xd."),
(35, "Actividad 2", "No se 2.0"),
(40, "Actividad 3", "No sé 3.0"),
(75, "Actividad 4", "No sé 4.0"),
(60, "Actividad 5", "No sé 5.0");

insert into passwd (passwd) values
("12345678"),
("password"),
("hola123"),
("qwertyu"),
("espaiderman");

select
concat("El usuario ", u.username, " ganó ", r.xp, " con ", r.accurate, "% de presición y una mejora del ", r.improvement, "% en ", a.name)
from user u
inner join result r on (u.id = r.id_user)
inner join activity a on (r.id_activity = a.id)

select
concat("Información de usuario: nombre: ", name, ", nombre de usuario: ", username, ", email: ", email, ", fecha de creación: ", date_)
from user

select
concat("El usuario ", u.username, " ha ganado ", p.xp, " de xp con ", p.accurate, "% de presición y una mejora del ", p.improvement, "%")
from user u
inner join progress p on (u.id = p.id_user)

select
concat("El usuario ", u.username, " ha donado $", p.amount, " USD")
from user u
inner join premium p on (u.id = p.id_user)