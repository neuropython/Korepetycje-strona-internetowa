from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
import os
from forms import CreatePostForm, LoginForm, UczenRegisterForm,KorepetytorRegisterForm , CommentForm
from classes import db, Post, Uczen, Korepetytor


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_KEY']
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id, who):
    if who == 'u':
        return db.get_or_404(Uczen, user_id)
    elif who == 'k':
        return db.get_or_404(Korepetytor, user_id)


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
db.init_app(app)


with app.app_context():
    db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register')
def register_uczen():
    form = UczenRegisterForm

    return render_template('register.html', form=form)


@app.route('/login')
def login_uczen():
    pass

@app.route('/login')
def login_korepetytor():
    pass


if __name__ == "__main__":
    app.run(debug=True)
