from datetime import datetime

from flask import Blueprint, request, redirect, render_template, url_for, session

import data_manager
import user_data_manager

answer_blueprint = Blueprint('answer', __name__, url_prefix='/answer')


@answer_blueprint.get("/<question_id>")
def show_add_answer_form(question_id):
    return render_template('answer.html', requested_answer=None, question_id=question_id)


@answer_blueprint.post("/<question_id>")
def add_answer(question_id):
    time = datetime.now()
    message = request.form.get('message')
    image = data_manager.upload_image()
    data_manager.add_answer(message, time, image, question_id)
    return redirect(url_for('question.show_question', question_id=question_id, view='no'))

@answer_blueprint.get('/<answer_id>/edit/<question_id>')
def show_edit_answer_form(answer_id, question_id):
    answer = data_manager.get_answer_by_id(answer_id, )
    return render_template('edit_answer.html', answer=answer, question_id=question_id)


@answer_blueprint.post('/<answer_id>/edit/<question_id>')
def edit_answer(answer_id, question_id):
    message = request.form.get('message')
    image = request.files['picture']
    if image:
        image = data_manager.upload_image()
    else:
        image = data_manager.get_image_to_answer(answer_id)
        image = image['image']
    time = datetime.now()
    data_manager.update_answer(answer_id, message, image, time)
    return redirect(url_for('question.show_question', question_id=question_id, view='no'))



@answer_blueprint.route("/<answer_id>/vote/<type_of_vote>/<question_id>")
def vote_answer(answer_id, type_of_vote, question_id):
    answer = data_manager.get_answer_by_id(answer_id)
    user_id = answer['user_id']
    user_data_manager.update_honor_answer(user_id, type_of_vote)
    honor = user_data_manager.get_own_honor()
    session['honor'] = honor['honor']
    data_manager.change_vote_answer(answer_id, type_of_vote)
    return redirect(url_for("question.show_question", question_id=question_id, view='no'))


@answer_blueprint.route('/delete/<answer_id>/<question_id>')
def delete_answer(question_id, answer_id):
    data_manager.delete_answer(answer_id)
    return redirect(url_for('question.show_question', question_id=question_id, view='no'))


@answer_blueprint.route('/accept/<answer_id>/<question_id>')
def accept_answer(answer_id, question_id):
    answer = data_manager.get_answer_by_id(answer_id)
    user_id = answer['user_id']
    user_data_manager.update_honor_answer(user_id, 'accept')
    honor = user_data_manager.get_own_honor()
    session['honor'] = honor['point']
    data_manager.accept_answer(answer_id)
    return redirect(url_for("question.show_question", question_id=question_id, vote='no'))


@answer_blueprint.route('/reject/<answer_id>/<question_id>')
def reject_answer(answer_id, question_id):
    answer = data_manager.get_answer_by_id(answer_id)
    user_id = answer['user_id']
    user_data_manager.update_honor_answer(user_id, 'reject')
    honor = user_data_manager.get_own_honor()
    session['honor'] = honor['point']
    data_manager.reject_answer(answer_id)
    return redirect(url_for("show_question", question_id=question_id, vote='no'))
