DROP TABLE IF EXISTS users_data;
create table users_data
(
    "id "     serial
        constraint users_data_pk
            primary key,
    user_name varchar not null,
    email     varchar not null,
    password  varchar not null,
    honor     int,
    role      varchar not null,
    registration_date timestamp without time zone
);

create unique index users_data_email_uindex
    on users_data (email);

create unique index users_data_user_name_uindex
    on users_data (user_name);




)