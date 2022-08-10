import databases_common
from flask import session

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
def update_honor_question(cursor, user_name, vote):
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
    elif vote == 'accept':
        query = """
                UPDATE users_data
                SET honor = honor + 15
                WHERE users_data.user_name = %(user_name)s"""
    elif vote == 'reject':
        query = """
                    UPDATE users_data
                    SET honor = honor - 15
                    WHERE users_data.user_name = %(user_name)s"""

    cursor.execute(query, {"user_name": user_name})


@databases_common.connection_handler
def select_name_by_question(cursor, question_id):
    cursor.execute("""
            SELECT question.user_name
            FROM question
            WHERE question.id = %(id)s""",
                   {'id': question_id})
    return cursor.fetchone()


@databases_common.connection_handler
def select_name_by_answer(cursor, answer_id):
    cursor.execute("""
            SELECT user_name 
            FROM answer
            WHERE id = %(id)s""",
                   {'id': answer_id})
    return cursor.fetchone()


@databases_common.connection_handler
def get_honor_by_username(cursor):
    cursor.execute("""
    SELECT honor FROM users_data
    WHERE user_name = %(name)s""",
                   {'name': session['username']})
    return cursor.fetchone()
