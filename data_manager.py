import os

import psycopg2.errors
from psycopg2 import sql
from werkzeug.utils import secure_filename

import databases_common
from flask import request, session

ALLOWED_EXTENSIONS = {"jpg", "png"}

UPLOAD_FOLDER = 'static/image/'


@databases_common.connection_handler
def show_all_question(cursor, order_by, order_direction):
    query = sql.SQL("SELECT * FROM question ORDER BY {} {};").format(sql.Identifier(order_by), sql.SQL(order_direction))
    cursor.execute(query)
    return cursor.fetchall()


@databases_common.connection_handler
def show_five_latest(cursor):
    cursor.execute("""
        SELECT * FROM question
        ORDER BY submission_time DESC LIMIT 5""")
    return cursor.fetchall()


@databases_common.connection_handler
def get_question(cursor, data_id):
    cursor.execute("""SELECT * FROM question
                        WHERE id = %(id)s""",
                   {"id": data_id})
    return cursor.fetchone()


@databases_common.connection_handler
def get_answer(cursor, answer_id):
    cursor.execute("""
    SELECT *
    FROM answer
    WHERE id = %(answer_id)s""",
                   {"answer_id": answer_id})
    return cursor.fetchone()


@databases_common.connection_handler
def get_comment(cursor, comment_id):
    cursor.execute("""
    SELECT *
    FROM comment
    WHERE id = %(comment_id)s""",
                   {"comment_id": comment_id})
    return cursor.fetchone()


# get data corresponding something
@databases_common.connection_handler
def get_answers_for_question(cursor, data_id):
    cursor.execute("""SELECT * FROM answer
                    WHERE answer.question_id = %(id)s
                    ORDER BY answer.accepted DESC, answer.submission_time DESC""",
                   {"id": data_id})
    return cursor.fetchall()


@databases_common.connection_handler
def get_comment_for_question(cursor, data_id):
    cursor.execute("""SELECT * FROM comment
                    WHERE comment.question_id = %(id)s
                    ORDER BY comment.submission_time DESC;""",
                   {"id": data_id})
    return cursor.fetchall()


@databases_common.connection_handler
def get_comment_for_answer(cursor, data_id):
    cursor.execute("""SELECT * FROM comment
                    WHERE comment.answer_id = %(id)s
                    ORDER BY comment.submission_time DESC;""",
                   {"id": data_id})
    return cursor.fetchall()


# add data

@databases_common.connection_handler
def add_question(cursor, title, message, time, image):
    cursor.execute("""
            INSERT INTO question(user_name, title, message, submission_time, vote_number, view_number, image)
             VALUES
            (%(name)s, %(title)s, %(message)s, %(time)s, 0, 0, %(image)s)
            RETURNING id
            """,
                   {'name': session['username'], 'title': title, 'message': message, 'time': time, 'image': image})
    return cursor.fetchone()


@databases_common.connection_handler
def add_answer(cursor, message, time, image, question_id):
    cursor.execute("""
    INSERT INTO answer(user_name, submission_time, vote_number, question_id, message, image)
    VALUES( %(name)s, %(time)s, 0, %(question_id)s, %(message)s, %(image)s )""",
                   {'name': session['username'], 'time': time, 'question_id': question_id, 'message': message,
                    'image': image})


@databases_common.connection_handler
def add_comment(cursor, question_id, message, submission_time, edited_count=0):
    query = """
                INSERT INTO comment (user_name, question_id, message, submission_time, edited_count)
                VALUES (%(name)s, %(question_id)s, %(message)s, %(submission_time)s, %(edited_count)s)
                """
    args = {'name': session['username'], 'question_id': question_id, 'message': message,
            'submission_time': submission_time, 'edited_count': edited_count
            }
    cursor.execute(query, args)


# add data corresponding something
@databases_common.connection_handler
def comment_answer(cursor, answer_id, message, submission_time):
    query = """
            INSERT INTO comment (user_name, answer_id, message,submission_time,edited_count)
            VALUES (%(name)s, %(answer_id)s,%(message)s,%(submission_time)s, 0)
            RETURNING id;
            """

    args = {'name': session['username'], 'answer_id': answer_id, 'message': message, 'submission_time': submission_time}
    cursor.execute(query, args)


# update data
@databases_common.connection_handler
def update_question(cursor, title, message, image, id):
    query = """
            UPDATE question
            SET title = %(title)s, message = %(message)s, image = %(image)s
            WHERE id = %(id)s
            """
    args = {'title': title, 'message': message, 'image': image, 'id': id}
    cursor.execute(query, args)


@databases_common.connection_handler
def update_comment(cursor, comment_id, message, time):
    query = """
            UPDATE comment
            SET message = %(message)s, submission_time = %(time)s, edited_count = edited_count + 1
            WHERE id = %(id)s;
            """
    args = {'id': comment_id, 'message': message, 'time': time}
    cursor.execute(query, args)


@databases_common.connection_handler
def update_answer(cursor, id, message, image, submission_time):
    query = """
            UPDATE answer
            SET message = %(message)s, image = %(image)s, submission_time = %(submission_time)s
            WHERE id = %(id)s
            """
    args = {'message': message, 'image': image, 'submission_time': submission_time, 'id': id}
    cursor.execute(query, args)


@databases_common.connection_handler
def update_tags(cursor, tags):
    for tag in tags:
        try:
            cursor.execute("""
            INSERT INTO tag (name)
            VALUES (%(tag)s);
            """, {"tag": tag})
        except psycopg2.errors.UniqueViolation:
            continue


# delete something
@databases_common.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE  FROM question
                    WHERE id = %(question_id)s""", {'question_id': question_id})


@databases_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""DELETE FROM answer
                    WHERE answer.id = %(answer_id)s""", {'answer_id': answer_id})


@databases_common.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute("""DELETE FROM comment
                    WHERE comment.id = %(comment_id)s""", {'comment_id': comment_id})


@databases_common.connection_handler
def delete_comment_by_answer(cursor, comment_id):
    cursor.execute("""DELETE FROM comment
                    WHERE comment.id = %(comment_id)s""", {'comment_id': comment_id})


@databases_common.connection_handler
def delete_tag(cursor, question_id, tag_id):
    cursor.execute("""
    DELETE FROM question_tag
    WHERE question_tag.question_id = %(question_id)s AND question_tag.tag_id = %(tag_id)s""",
                   {"question_id": question_id, "tag_id": tag_id})


# utility

@databases_common.connection_handler
def change_vote_question(cursor, question_id, vote):
    if vote == "down":
        query = "UPDATE question SET vote_number = vote_number - 1 WHERE question.id = %(question_id)s"
    elif vote == "up":
        query = "UPDATE question SET vote_number = vote_number + 1 WHERE question.id = %(question_id)s"
    cursor.execute(query, {"question_id": question_id})


@databases_common.connection_handler
def change_vote_answer(cursor, answer_id, vote):
    if vote == "down":
        query = "UPDATE answer SET vote_number = vote_number - 1 WHERE answer.id = %(answer_id)s"
    elif vote == "up":
        query = "UPDATE answer SET vote_number = vote_number + 1 WHERE answer.id = %(answer_id)s"
    cursor.execute(query, {"answer_id": answer_id})


@databases_common.connection_handler
def increase_view(cursor, data_id):
    cursor.execute("""UPDATE question 
                    SET view_number = view_number + 1 
                    WHERE id = %(id)s""",
                   {"id": data_id})


@databases_common.connection_handler
def get_image_to_answer(cursor, answer_id):
    cursor.execute("""
    SELECT answer.image as image FROM answer
    WHERE answer.id = %(answer_id)s""",
                   {'answer_id': answer_id})
    return cursor.fetchone()


@databases_common.connection_handler
def get_image_to_question(cursor, question_id):
    cursor.execute("""
    SELECT question.image as image FROM question
    WHERE question.id = %(question_id)s""",
                   {'question_id': question_id})
    return cursor.fetchone()


def get_answers_and_comments(question):
    answers = get_answers_for_question(question['id'])
    comment_of_question = get_comment_for_question(question['id'])
    comment_of_answer = [get_comment_for_answer(answer['id']) for answer in answers]
    return answers, comment_of_question, comment_of_answer


# search feature
@databases_common.connection_handler
def get_searched_question(cursor, search):
    cursor.execute("""
    SELECT DISTINCT question.* FROM question 
    LEFT JOIN answer on question.id = answer.question_id
    WHERE question.message ILIKE %(search)s OR question.title ILIKE %(search)s OR answer.message ILIKE %(search)s ;
    """,
                   {"search": "%" + str(search) + "%"})
    return cursor.fetchall()


# upload image
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_image():
    file = request.files['picture']
    if file.filename == "":
        return ""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return filename


# tags

@databases_common.connection_handler
def get_tags_for_question(cursor, q_id):
    cursor.execute("""
    SELECT * FROM tag
    JOIN question_tag qt on tag.id = qt.tag_id
    WHERE qt.question_id = %(q_id)s""",
                   {"q_id": q_id})
    return cursor.fetchall()


@databases_common.connection_handler
def add_tags(cursor, tags, question_id):
    id_of_tags = []
    for tag in tags:
        cursor.execute("""
        SELECT id FROM tag
        WHERE name = %(tag)s""",
                       {'tag': tag})
        id_of_tags.append(cursor.fetchone())

    for id_of_tag in id_of_tags:
        cursor.execute("""
        INSERT INTO question_tag (question_id, tag_id)
        VALUES (%(question_id)s, %(id_of_tag)s)""",
                       {'question_id': question_id, 'id_of_tag': id_of_tag['id']})


@databases_common.connection_handler
def get_all_tags(cursor):
    cursor.execute("""
    SELECT tag.name, COUNT(question_id) as q_count FROM tag
    join question_tag qt on tag.id = qt.tag_id
    GROUP BY  tag.name""")
    return cursor.fetchall()


@databases_common.connection_handler
def accept_answer(cursor, answer_id):
    cursor.execute("""
            UPDATE answer
            SET accepted = true
            WHERE answer.id = %(answer_id)s""",
                   {"answer_id": answer_id})


@databases_common.connection_handler
def reject_answer(cursor, answer_id):
    cursor.execute("""
            UPDATE answer
            SET accepted = false
            WHERE answer.id = %(answer_id)s""",
                   {"answer_id": answer_id})
