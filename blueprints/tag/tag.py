from flask import Blueprint, request, render_template, redirect, url_for

import data_manager

tag_blueprint = Blueprint('tag', __name__)


@tag_blueprint.route('/add_tag/<question_id>', methods=['GET', 'POST'])
def add_tag(question_id):
    if request.method == 'GET':
        return render_template('add_tag.html', question_id=question_id)
    elif request.method == 'POST':
        tags = set(request.form.get('tag').split())
        data_manager.update_tags(tags)
        data_manager.add_tags(tags, question_id)
        return redirect(url_for('show_question', question_id=question_id))


@tag_blueprint.route('/delete/<question_id>/<tag_id>/delete_tag')
def delete_tag(question_id, tag_id):
    data_manager.delete_tag(question_id, tag_id)
    return redirect(url_for("show_question", question_id=question_id, view="no"))


@tag_blueprint.route('/tags')
def show_tags():
    tags = data_manager.get_all_tags()
    return render_template('tags.html', tags=tags)
