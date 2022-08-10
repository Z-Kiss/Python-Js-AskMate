import os

import psycopg2.errors
from psycopg2 import sql
from werkzeug.utils import secure_filename

import databases_common
from flask import request

import utils


@databases_common.connection_handler
def register(cursor, username, email, password):
    password = utils.hash_password(password)
    query = """
            INSERT INTO users_data (user_name, email, password, honor, role)
            VALUES ( %(user_name)s, %(email)s, %(password)s, 0, 1)
            """
    args = {'user_name': username, 'email': email, 'password': password}
    cursor.execute(query, args)

@databases_common.connection_handler
def get_user_data_by_email(cursor, email):
    cursor.execute("""
    SELECT * FROM users_data
    WHERE email = %(email)s""",
                   {'email': email})
    return cursor.fetchone()


@databases_common.connection_handler
def list_all_users(cursor):
    query = """
            SELECT users_data.*, COUNT(question.id) as "Number of questions"
            FROM users_data
            INNER JOIN question
                ON users_data."id " = question.user_id
            group by users_data."id ";"""
    cursor.execute(query)
    return cursor.fetchall()

