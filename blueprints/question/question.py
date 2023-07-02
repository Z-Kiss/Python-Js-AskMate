from datetime import datetime

from flask import Blueprint, request, render_template, redirect, url_for, session

import data_manager
import user_data_manager

question_blueprint = Blueprint('question', __name__)


@question_blueprint.route("/list", methods=['GET', 'POST'])
def show_all_questions():
    if request.method == 'GET':
        questions = data_manager.show_all_question()
    elif request.method == 'POST':
        order_by = request.form.get('order_by')
        order_direction = request.form.get('order_direction')
        questions = data_manager.show_all_question(order_by, order_direction)
    tags = [data_manager.get_tags_for_question(question['id']) for question in questions]
    return render_template("show_all_question.html", questions=questions, tags=tags)


@question_blueprint.route("/question/<question_id>")
def show_question(question_id):
    if request.args.get('view') != "no":
        data_manager.increase_view(question_id)
    question = data_manager.get_question(question_id)
    answers, comment_of_question, comment_of_answer = data_manager.get_answers_and_comments(question)
    tags = data_manager.get_tags_for_question(question_id)
    return render_template("show_question.html", question=question, tags=tags,
                           comment_of_question=comment_of_question, answers=answers,
                           comment_of_answer=comment_of_answer)


@question_blueprint.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == 'POST':
        time = datetime.now()
        title = request.form.get('title')
        message = request.form.get('message')
        image = data_manager.upload_image()
        q_id = data_manager.add_question(title, message, time, image)
        tags = request.form.get('tag').split()
        data_manager.update_tags(tags)
        data_manager.add_tags(tags, q_id['id'])
    elif request.method == 'GET':
        return render_template('ask_edit_question.html', requested_question=None)
    return redirect("/")


@question_blueprint.route('/question/<question_id>/edit', methods=["GET", "POST"])
def edit_question(question_id):
    if request.method == 'POST':
        image = request.files['picture']
        if image:
            image = data_manager.upload_image()
        else:
            image = data_manager.get_image_to_question(question_id)
            image = image['image']
        data_manager.update_question(request.form.get('title'), request.form.get('message'), image, question_id)
        return redirect(url_for('show_question', question_id=question_id))
    question = data_manager.get_question(question_id)
    return render_template('ask_edit_question.html', question=question)


@question_blueprint.route("/delete/question/<question_id>")
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for('show_all_questions'))


@question_blueprint.route("/question/search", methods=['GET', 'POST'])
def search_question():
    if request.method == 'GET':
        return render_template("search_result.html", questions=None)
    elif request.method == 'POST':
        search = request.form.get('search')
        questions = data_manager.get_searched_question(search)
        for question in questions:
            question['title'] = question['title'].replace(search, "<strong> " + search + " </strong>")
            question['message'] = question['message'].replace(search, "<strong> " + search + " </strong>")
        tags = [data_manager.get_tags_for_question(question['id']) for question in questions]
        return render_template("search_result.html", questions=questions, tags=tags)


@question_blueprint.route("/question/<question_id>/vote/<type_of_vote>")
def vote_question(question_id, type_of_vote):
    user_name = user_data_manager.select_name_by_question(question_id)
    user_data_manager.update_honor_question(user_name['user_name'], type_of_vote)
    honor = user_data_manager.get_honor_by_username()
    session['honor'] = honor['honor']
    data_manager.change_vote_question(question_id, type_of_vote)
    return redirect(url_for("show_question", question_id=question_id))
