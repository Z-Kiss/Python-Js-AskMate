--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6
DROP TABLE IF EXISTS users_data CASCADE ;
create table users_data (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR NOT NULL,
    email     VARCHAR NOT NULL,
    password  VARCHAR NOT NULL,
    honor     INT,
    role      VARCHAR NOT NULL,
    registration_date TIMESTAMP WITHOUT TIME ZONE
);

DROP TABLE IF EXISTS question CASCADE ;
CREATE TABLE question (
    id SERIAL PRIMARY KEY,
    user_name TEXT NOT NULL,
    user_id INT REFERENCES users_data ON DELETE CASCADE ,
    submission_time TIMESTAMP WITHOUT TIME ZONE,
    view_number INT,
    vote_number INT,
    title TEXT,
    message TEXT,
    image TEXT
);

DROP TABLE IF EXISTS answer CASCADE ;
CREATE TABLE answer (
    user_name TEXT NOT NULL,
    id SERIAL PRIMARY KEY,
    submission_time TIMESTAMP WITHOUT TIME ZONE,
    vote_number INT,
    question_id INT REFERENCES question(id) ON DELETE CASCADE,
    message TEXT,
    image TEXT,
    accepted BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS comment CASCADE ;
CREATE TABLE comment (
    user_name TEXT NOT NULL,
    id SERIAL PRIMARY KEY,
    question_id INT REFERENCES question(id) ON DELETE CASCADE ,
    answer_id INT REFERENCES answer(id) ON DELETE CASCADE ,
    message TEXT,
    submission_time TIMESTAMP WITHOUT TIME ZONE,
    edited_count INT
);

DROP TABLE IF EXISTS tag CASCADE ;
CREATE TABLE tag (
id SERIAL PRIMARY KEY,
name TEXT UNIQUE
);


DROP TABLE IF EXISTS question_tag CASCADE ;
CREATE TABLE question_tag (
question_id INT NOT NULL REFERENCES question(id) ON DELETE CASCADE,
tag_id INT NOT NULL REFERENCES tag(id)
);

