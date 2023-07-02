from datetime import datetime

from flask import Blueprint, request, render_template, redirect, url_for, session

import data_manager
import user_data_manager

question_blueprint = Blueprint('question', __name__, url_prefix='/question')


@question_blueprint.get("/show")
def show_all_questions():
    order_by = request.args.get('order_by')
    if not order_by:
        order_by = 'submission_time'
    order_direction = request.args.get('order_direction')
    if not order_direction:
        order_direction = 'desc'
    questions = data_manager.show_all_question(order_by, order_direction)
    tags = [data_manager.get_tags_for_question(question['id']) for question in questions]
    return render_template("show_all_question.html", questions=questions, tags=tags)


@question_blueprint.get("/<question_id>")
def show_question(question_id):
    if request.args.get('view') != "no":
        data_manager.increase_view(question_id)
    question = data_manager.get_question_by_id(question_id, )
    answers, comment_of_question, comment_of_answer = data_manager.get_answers_and_comments(question)
    tags = data_manager.get_tags_for_question(question_id)
    return render_template("show_question.html", question=question, tags=tags,
                           comment_of_question=comment_of_question, answers=answers,
                           comment_of_answer=comment_of_answer)


@question_blueprint.post("/add")
def add_question():
    time = datetime.now()
    title = request.form.get('title')
    message = request.form.get('message')
    image = data_manager.upload_image()
    question_id = data_manager.add_question(title, message, time, image)
    tags = request.form.get('tag').split()
    data_manager.update_tags(tags)
    data_manager.add_tags(tags, question_id['id'])
    return redirect("/")


@question_blueprint.get("/add")
def show_add_question_form():
    return render_template('ask_edit_question.html', question=None)


@question_blueprint.get('/edit/<question_id>')
def show_question_editor(question_id):
    question = data_manager.get_question_by_id(question_id, )
    return render_template('ask_edit_question.html', question=question)


@question_blueprint.post('/edit/<question_id>')
def edit_question(question_id):
    image = request.files['picture']
    if image:
        image = data_manager.upload_image()
    else:
        image = data_manager.get_image_to_question(question_id)
        image = image['image']
    data_manager.update_question(request.form.get('title'), request.form.get('message'), image, question_id)
    return redirect(url_for('question.show_question', question_id=question_id))


@question_blueprint.route("/delete/<question_id>")
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for('question.show_all_questions'))


@question_blueprint.get("/search")
def search_question():
    search_word = request.args.get('search')
    if not search_word:
        return render_template("search_result.html", questions=None)
    elif search_word:
        questions = data_manager.get_searched_question(search_word)
        for question in questions:
            question['title'] = question['title'].replace(search_word, "<strong> " + search_word + " </strong>")
            question['message'] = question['message'].replace(search_word, "<strong> " + search_word + " </strong>")
        tags = [data_manager.get_tags_for_question(question['id']) for question in questions]
        return render_template("search_result.html", questions=questions, tags=tags)


@question_blueprint.get("/vote/<question_id>/<type_of_vote>")
def vote_question(question_id, type_of_vote):
    question = data_manager.get_question_by_id(question_id)
    user_id = question['user_id']
    user_data_manager.update_honor_question(user_id, type_of_vote)
    current_honor = user_data_manager.get_own_honor()
    session['honor'] = current_honor['point']
    data_manager.change_vote_question(question_id, type_of_vote)
    return redirect(url_for("question.show_question", question_id=question_id, view="no"))
