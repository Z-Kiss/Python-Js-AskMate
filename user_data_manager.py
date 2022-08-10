import os

import psycopg2.errors
from psycopg2 import sql
from werkzeug.utils import secure_filename

import databases_common
from flask import request

import utils


@databases_common.connection_handler
def register(cursor, username, email, password, time):
    password = utils.hash_password(password)
    query = """
            INSERT INTO users_data (user_name, email, password, honor, role, registration_date)
            VALUES ( %(user_name)s, %(email)s, %(password)s, 0, 1, %(time)s)
            """
    args = {'user_name': username, 'email': email, 'password': password, 'time': time}
    cursor.execute(query, args)

@databases_common.connection_handler
def get_user_data_by_email(cursor, email):
    cursor.execute("""
    SELECT * FROM users_data
    WHERE email = %(email)s""",
                   {'email': email})
    return cursor.fetchone()


@databases_common.connection_handler
def update_honor_question(cursor, user_name, vote, ):
    if vote == "down":
        query = """
                UPDATE users_data 
                SET honor = honor - 2 
                WHERE users_data.user_name = %(user_name)s"""
    elif vote == "up":
        query = """
                UPDATE users_data 
                SET honor = honor + 5
                WHERE users_data.user_name = %(user_name)s"""
    cursor.execute(query, {"user_name": user_name})


@databases_common.connection_handler
def update_honor_answer(cursor, user_name, vote):
    if vote == "down":
        query = """
                UPDATE users_data 
                SET honor = honor - 2 
                WHERE users_data.user_name = %(user_name)s"""
    elif vote == "up":
        query = """
                UPDATE users_data
                SET honor = honor + 10
                WHERE users_data.user_name = %(user_name)s"""
    cursor.execute(query, {"user_name": user_name})
