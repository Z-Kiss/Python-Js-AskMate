from dotenv import load_dotenv, find_dotenv
from flask import Flask, redirect, render_template, session
import data_manager

from blueprints.answer.answer import answer_blueprint
from blueprints.auth.auth import auth_blueprint
from blueprints.comment.comment import comment_blueprint
from blueprints.question.question import question_blueprint
from blueprints.tag.tag import tag_blueprint
from blueprints.user.user import user_blueprint

load_dotenv(find_dotenv("config.env"))
app = Flask(__name__)
app.config['SECRET_KEY'] = "lKhKNRzU8mIKfwpE4f3djINmV0zUL3Lu"

app.register_blueprint(answer_blueprint,)
app.register_blueprint(auth_blueprint)
app.register_blueprint(comment_blueprint)
app.register_blueprint(question_blueprint)
app.register_blueprint(tag_blueprint)
app.register_blueprint(user_blueprint)


@app.route("/")
def short_five_latest():
    if 'username' not in session:
        return redirect('/login')
    questions = data_manager.show_five_latest()
    tags = [data_manager.get_tags_for_question(question['id']) for question in questions]
    return render_template("show_all_question.html", questions=questions, tags=tags, user='Hi ' + session['username'])


if __name__ == '__main__':
    app.run(debug=True)
