from functools import wraps

import bcrypt
from flask import session, flash, redirect

import user_data_manager


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            flash('Need to be Logged in!')
            return redirect('/auth/login')
        else:
            user = user_data_manager.get_user_by_id(user_id)
            if not user:
                flash('Authentication failed')
                return redirect('/auth/login')
        return func(*args, **kwargs)
    return decorated
