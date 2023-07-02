from flask import Blueprint, session, render_template, redirect, url_for

import user_data_manager

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/users')
def list_users():
    if 'username' in session:
        users = user_data_manager.list_all_users()
        return render_template('users_list.html', users=users)
    return redirect(url_for('login'))


@user_blueprint.route('/users/<user_name>')
def show_user(user_name):
    get_user = user_data_manager.get_user_details(user_name)
    user_questions = user_data_manager.get_user_questions(get_user[0]['id'])
    user_answers = user_data_manager.get_user_answers(get_user[0]['id'])
    user_comments = user_data_manager.get_user_comments(get_user[0]['user_name'])
    return render_template('user_page.html', get_user=get_user, user_questions=user_questions,
                           user_answers=user_answers, user_comments=user_comments)
