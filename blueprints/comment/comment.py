from datetime import datetime

from flask import Blueprint, request, redirect, url_for, render_template

import data_manager

comment_blueprint = Blueprint('comment', __name__)


@comment_blueprint.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def new_comment(question_id):
    if request.method == 'POST':
        message = request.form.get('message')
        submission_time = datetime.now()
        edited_count = 0
        data_manager.add_comment(question_id, message, submission_time, edited_count)
        return redirect(url_for('show_question', question_id=question_id))
    return render_template('answer.html', id=question_id)


# comment to answer
@comment_blueprint.route("/answer/<answer_id>/new-comment/<question_id>", methods=['POST', 'GET'])
def new_comment_answer(answer_id, question_id):
    if request.method == 'POST':
        message = request.form.get('message')
        submission_time = datetime.now()
        data_manager.comment_answer(answer_id, message, submission_time)
        return redirect(url_for('show_question', question_id=question_id))
    return render_template('add_comment.html', answer_id=answer_id, question_id=question_id)


@comment_blueprint.route("/comment/<comment_id>/edit-comment/<question_id>", methods=['POST', 'GET'])
def edit_comment(comment_id, question_id):
    if request.method == 'POST':
        message = request.form.get('message')
        time = datetime.now()
        data_manager.update_comment(comment_id, message, time)
        return redirect(url_for("show_question", question_id=question_id))
    comment = data_manager.get_comment(comment_id)
    return render_template('edit_comment.html', comment=comment, question_id=question_id)


@comment_blueprint.route('/delete/question/comment/<comment_id>/<question_id>')
def delete_comment(comment_id, question_id):
    data_manager.delete_comment(comment_id)
    return redirect(url_for('show_question', question_id=question_id, view='no'))

# TODO change html link
# @comment_blueprint.route('/delete/answer/comment/<comment_id>/<question_id>')
# def delete_comment_by_answer(comment_id, question_id):
#     data_manager.delete_comment_by_answer(comment_id)
#     return redirect(url_for('show_question', question_id=question_id, view='no'))
