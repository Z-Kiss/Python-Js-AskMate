from flask import Blueprint, request, render_template, redirect, url_for

import data_manager
from utils import login_required

tag_blueprint = Blueprint('tag', __name__, url_prefix='/tag')


@tag_blueprint.get('/<question_id>')
@login_required
def show_add_tag_form(question_id):
    return render_template('add_tag.html', question_id=question_id)


@tag_blueprint.post('/<question_id>')
@login_required
def add_tag(question_id):
    tags = set(request.form.get('tag').split())
    data_manager.update_tags(tags)
    data_manager.add_tags(tags, question_id)
    return redirect(url_for('question.show_question', question_id=question_id))


@tag_blueprint.get('/delete/<question_id>/<tag_id>/')
@login_required
def delete_tag(question_id, tag_id):
    data_manager.delete_tag(question_id, tag_id)
    return redirect(url_for("question.show_question", question_id=question_id, view="no"))


@tag_blueprint.route('/tags')
@login_required
def show_tags():
    tags = data_manager.get_all_tags()
    return render_template('tags.html', tags=tags)
