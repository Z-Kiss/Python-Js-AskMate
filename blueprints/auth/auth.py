import datetime
import psycopg2
import psycopg2.errors
import user_data_manager
import utils

from flask import Blueprint, request, render_template, flash, redirect, session

auth_blueprint = Blueprint('auth,', __name__, url_prefix='/auth')


@auth_blueprint.route("/register", methods=['GET', 'POST'])
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


@auth_blueprint.route('/login', methods=['GET', 'POST'])
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


@auth_blueprint.route("/logout")
def logout():
    if 'username' in session:
        username = session['username']
        session.clear()
        flash(f"You have been logged out {username}")
        return redirect("/")
