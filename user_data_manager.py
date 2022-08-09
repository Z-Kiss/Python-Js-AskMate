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

