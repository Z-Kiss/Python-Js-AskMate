import flask
import datetime

import psycopg2.errors
from flask import Flask, request, redirect, flash, url_for, render_template,session
import data_manager
import user_data_manager
import utils

app = Flask(__name__)


app.config['SECRET_KEY'] = "francosize"


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        psw = request.form.get('password')
        time = datetime.datetime.now()
        try:
            user_data_manager.register(username, email, psw, time)
        except psycopg2.errors.UniqueViolation:
            flash('Username or Email already in use!')
        return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        psw = request.form.get('password')
        user_data = user_data_manager.get_user_data_by_email(email)
        if user_data:
            if utils.verify_password(psw, user_data['password']):
                session['username'] = user_data['user_name']
                session['role'] = user_data['role']
                session['honor'] = user_data['honor']
                return redirect('/')
            else:
                flash('Incorrect Password/email')
                return redirect('/login')
        else:
            flash('Incorrect Password/Email')
            return redirect('/login')
    elif request.method == 'GET':
        return render_template('login.html')


@app.route("/logout")
def logout():
    if 'username' in session:
        username = session['username']
        session.clear()
        flash(f"You have been logged out {username}")
        return redirect("/")


@app.route("/")
def short_five_latest():
    if 'username' not in session:
        return redirect('/login')
    questions = data_manager.show_five_latest()
    tags = [data_manager.get_tags_for_question(question['id']) for question in questions]
    return render_template("show_all_question.html", questions=questions, tags=tags, user='Hi ' + session['username'])


@app.route("/list", methods=['GET','POST'])
def show_all_questions():
    if request.method == 'GET':
        questions = data_manager.show_all_question()
    elif request.method == 'POST':
        order_by = request.form.get('order_by')
        order_direction = request.form.get('order_direction')
        questions = data_manager.show_all_question(order_by, order_direction)
    tags = [data_manager.get_tags_for_question(question['id']) for question in questions]
    return flask.render_template("show_all_question.html", questions=questions, tags=tags)


@app.route("/question/<question_id>")
def show_question(question_id):
    if request.args.get('view') != "no":
        data_manager.increase_view(question_id)
    question = data_manager.get_question(question_id)
    answers, comment_of_question, comment_of_answer = data_manager.get_answers_and_comments(question)
    tags = data_manager.get_tags_for_question(question_id)
    return flask.render_template("show_question.html", question=question, tags=tags,
                                 comment_of_question=comment_of_question, answers=answers,
                                 comment_of_answer=comment_of_answer)


@app.route("/delete/question/<question_id>")
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for('show_all_questions'))


@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == 'POST':
        time = datetime.datetime.now()
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


@app.route('/add_tag/<question_id>', methods=['GET', 'POST'])
def add_tag(question_id):
    if request.method == 'GET':
        return render_template('add_tag.html', question_id=question_id)
    elif request.method == 'POST':
        tags = set(request.form.get('tag').split())
        data_manager.update_tags(tags)
        data_manager.add_tags(tags, question_id)
        return redirect(url_for('show_question', question_id=question_id))


@app.route("/add_answer/<question_id>", methods=["GET", "POST"])
def add_answer(question_id):
    if request.method == 'POST':
        time = datetime.datetime.now()
        message = request.form.get('message')
        data_manager.add_answer(message, time, question_id)
        return redirect(url_for('show_question', question_id=question_id))
    elif request.method == 'GET':
        return render_template('answer.html', requested_answer=None, question_id=question_id)


@app.route('/question/<question_id>/new-comment', methods=['POST', 'GET'])
def new_comment(question_id):
    if request.method == 'POST':
        message = request.form.get('message')
        submission_time = datetime.datetime.now()
        edited_count = 0
        data_manager.add_comment(question_id, message, submission_time, edited_count)
        return redirect(url_for('show_question', question_id=question_id))
    return render_template('answer.html', id=question_id)


@app.route("/answer/<answer_id>/new-comment/<question_id>", methods=['POST', 'GET'])
def new_comment_answer(answer_id, question_id):
    if request.method == 'POST':
        message = request.form.get('message')
        submission_time = datetime.datetime.now()
        data_manager.comment_answer(answer_id, message, submission_time)
        return redirect(url_for('show_question', question_id=question_id))
    return render_template('add_comment.html', answer_id=answer_id, question_id=question_id)


@app.route('/question/<question_id>/edit', methods=["GET", "POST"])
def edit_question(question_id):
    if request.method == 'POST':
        data_manager.update_question(request.form.get('title'), request.form.get('message'), request.form.get('image'), question_id)
        return redirect(url_for('show_question', question_id=question_id))
    question = data_manager.get_question(question_id)
    return render_template('ask_edit_question.html', question=question)


@app.route('/answer/<answer_id>/edit/<question_id>', methods=["GET", "POST"])
def edit_answer(answer_id, question_id):
    if request.method == 'POST':
        message = request.form.get('message')
        image = request.form.get('image')
        time = datetime.datetime.now()
        data_manager.update_answer(answer_id, message, image, time)
        return redirect(url_for('show_question', question_id=question_id))
    answer = data_manager.get_answer(answer_id)
    return render_template('edit_comment.html', answer=answer, question_id=question_id)


@app.route("/comment/<comment_id>/edit-comment/<question_id>", methods=['POST', 'GET'])
def edit_comment(comment_id, question_id):
    if request.method == 'POST':
        message = request.form.get('message')
        time = datetime.datetime.now()
        data_manager.update_comment(comment_id, message, time)
        return redirect(url_for("show_question", question_id=question_id))
    comment = data_manager.get_comment(comment_id)
    return render_template('edit_answer.html', comment=comment, question_id=question_id)


@app.route("/question/<question_id>/vote/<type_of_vote>")
def vote_question(question_id, type_of_vote):
    user_name = user_data_manager.select_name_by_question(question_id)
    user_data_manager.update_honor_question(user_name['user_name'], type_of_vote)
    honor = user_data_manager.get_honor_by_username()
    session['honor'] = honor['honor']
    data_manager.change_vote_question(question_id, type_of_vote)
    return redirect(url_for("show_question", question_id=question_id))


@app.route("/answer/<answer_id>/vote/<type_of_vote>/<question_id>")
def vote_answer(answer_id, type_of_vote, question_id):
    user_name = user_data_manager.select_name_by_answer(answer_id)
    user_data_manager.update_honor_answer(user_name['user_name'], type_of_vote)
    honor = user_data_manager.get_honor_by_username()
    session['honor'] = honor['honor']
    data_manager.change_vote_answer(answer_id, type_of_vote)
    return redirect(url_for("show_question", question_id=question_id))


@app.route("/question/search", methods=['GET', 'POST'])
def search_question():
    if request.method == 'GET':
        return flask.render_template("search_result.html", questions=None)
    elif request.method == 'POST':
        search = request.form.get('search')
        questions = data_manager.get_searched_question(search)
        for question in questions:
            question['title'] = question['title'].replace(search, "<strong> " + search + " </strong>")
            question['message'] = question['message'].replace(search, "<strong> " + search + " </strong>")
        tags = [data_manager.get_tags_for_question(question['id']) for question in questions]
        return flask.render_template("search_result.html", questions=questions, tags=tags)


@app.route('/delete/question/comment/<comment_id>/<question_id>')
def delete_comment(comment_id, question_id):
    data_manager.delete_comment(comment_id)
    return redirect(url_for('show_question', question_id=question_id, view='no'))


@app.route('/delete/answer/comment/<comment_id>/<question_id>')
def delete_comment_by_answer(comment_id, question_id):
    data_manager.delete_comment_by_answer(comment_id)
    return redirect(url_for('show_question', question_id=question_id, view='no'))


@app.route('/delete/question/answer/<answer_id>/<question_id>')
def delete_answer(question_id, answer_id):
    data_manager.delete_answer(answer_id)
    return redirect(url_for('show_question', question_id=question_id, view='no'))


@app.route('/delete/<question_id>/<tag_id>/delete_tag')
def delete_tag(question_id, tag_id):
    data_manager.delete_tag(question_id, tag_id)
    return redirect(url_for("show_question", question_id=question_id, view="no"))


@app.route('/accept/<answer_id>/<user_name>/<question_id>')
def accept_answer(answer_id, user_name, question_id):
    data_manager.accept_answer(answer_id)
    user_data_manager.update_honor_answer(user_name, 'accept')
    return redirect(url_for("show_question", question_id=question_id))

@app.route('/reject/<answer_id>/<user_name>/<question_id>')
def reject_answer(answer_id, user_name, question_id):
    data_manager.reject_answer(answer_id)
    user_data_manager.update_honor_answer(user_name, 'reject')
    return redirect(url_for("show_question", question_id=question_id))

@app.route('/tags')
def show_tags():
    tags = data_manager.get_all_tags()
    return render_template('tags.html', tags=tags)

if __name__ == '__main__':
    app.run(debug=True)
