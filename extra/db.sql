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
    difficult int not null,
    path_game varchar(255) not null,
    constraint pk primary key (id)
)

create table result (
    id int auto_increment,
    xp int not null,
    accurate float not null,
    date_ datetime not null,
    id_user int not null,
    id_activity int not null,
    constraint pk primary key (id),
    constraint fk_user_res foreign key (id_user) references user (id) on delete cascade,
    constraint fk_activity_res foreign key (id_activity) references activity (id)
)

--passwd: 12345678
insert into user (name, username, passwd, date_, email, role, strike) values
("negatron_griffin", "negatron", "$2b$12$.3Q5L4BTQDMMvx7IbEPkb.xOCl10Gr7TiDSDtZ5GRw4qXh/we1aGO", '2000-01-01', "admin@nega.com", 9999, 0)

insert into activity (xp, name, description, difficult, path_game) values
(
    300,
    "Atrapa el Dinero",
    "Atrape todo el dinero que cae.\nEl personaje se controla con las teclas A, D, Flecha Izquierda y Flecha Derecha.\nEste es un ejercicio básico que estimula movimientos báscos en los dedos y puede ser usado como calentamiento al ser el más básico.",
    1,
    "catch_money")

insert into activity (xp, name, description, difficult, path_game) values (
    500,
    "Golpea al Topo",
    "Deberá golpear los TOPOS que aparezcan.\nRequiere que el usuario pueda mover el ratón sin mucha dificultad.\nAyuda a mejorar los reflejos de las manos y precisión al realizar una acción.\nSE RECOMIENDA INTERCALAR LAS MANOS.",
    3,
    "whack_mole"
)

insert into activity (xp, name, description, difficult, path_game) values (
    400,
    "FridaiNaiFunki",
    "Deberá acertar las flechas en el momento adecuado.\nSe puede utilizar tanto las flechas como las teclas WASD.\nAyuda a mejorar la reacción básica básica, cordinación ojo-mano y memoria muscular.",
    2,
    "fnf_game"
)

insert into activity (xp, name, description, difficult, path_game) values (
    500,
    "Ejercicio Físico",
    "¿Requiere de algo más serio?\nIntente realizar estos ejercicios los cuales también ayudan y son más efectivos si se practican a diario, fortalecen las muñecas y dedos.\nREQUIERE DE WEBCAM.\n\nEsta es una fase beta, puede provocar errores.",
    1,
    "no_game"
)

select * from passwd

insert into passwd (passw) values ("xd")