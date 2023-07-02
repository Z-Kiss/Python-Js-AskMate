from datetime import datetime

from flask import Blueprint, request, redirect, url_for, render_template

import data_manager

comment_blueprint = Blueprint('comment', __name__, url_prefix='/comment')


@comment_blueprint.get('/<question_id>')
@comment_blueprint.get('/<question_id>/<answer_id>')
def show_new_comment_form(question_id, answer_id=None):
    return render_template('add_comment.html', question_id=question_id, answer_id=answer_id)


@comment_blueprint.post('/question/<question_id>')
def add_new_comment_to_question(question_id):
    message = request.form.get('message')
    submission_time = datetime.now()
    data_manager.add_comment_to_question(question_id, message, submission_time)
    return redirect(url_for('question.show_question', question_id=question_id, vote='no'))


@comment_blueprint.post("/answer/<answer_id>/<question_id>")
def add_new_comment_to_answer(answer_id, question_id):
    message = request.form.get('message')
    submission_time = datetime.now()
    data_manager.add_comment_to_answer(answer_id, message, submission_time)
    return redirect(url_for('question.show_question', question_id=question_id, vote='no'))


@comment_blueprint.get("/edit/<comment_id>/<question_id>")
def show_edit_comment_form(comment_id, question_id):
    comment = data_manager.get_comment(comment_id)
    return render_template('edit_comment.html', comment=comment, question_id=question_id)


@comment_blueprint.post("/edit/<comment_id>/<question_id>")
def edit_comment(comment_id, question_id):
    message = request.form.get('message')
    time = datetime.now()
    data_manager.update_comment(comment_id, message, time)
    return redirect(url_for("question.show_question", question_id=question_id, vote='no'))



@comment_blueprint.route('/delete/<comment_id>/<question_id>')
def delete_comment(comment_id, question_id):
    data_manager.delete_comment(comment_id)
    return redirect(url_for('question.show_question', question_id=question_id, view='no'))
