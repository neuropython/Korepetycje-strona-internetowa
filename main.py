from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
import os
from forms import CreatePostForm, LoginForm, UczenRegisterForm,KorepetytorRegisterForm , CommentForm
from classes import db, Post, Uczen, Korepetytor


app = Flask(__name__)
app.config['SECRET_KEY'] = 'saiufdgsaiuhfoisandfbvsai'
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


@app.route('/main')
def main():
    return render_template("index.html")


@app.route('/register/<mode>', methods=["GET", "POST"])
def register(mode):
    if mode == 'u':
        form = UczenRegisterForm()
        if form.validate_on_submit():

            # Check if user email is already present in the database.
            result = db.session.execute(db.select(Uczen).where(Uczen.email == form.email.data))
            user = result.scalar()
            if user:
                # User already exists
                flash("You've already signed up with that email, log in instead!")
                return redirect(url_for('login', mode=mode))

            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = Uczen(
                email=form.email.data,
                name=form.name.data,
                surname=form.surname.data,
                password=hash_and_salted_password,
                phone_number=form.phone_number.data,
            )
            db.session.add(new_user)
            db.session.commit()
            # This line will authenticate the user with Flask-Login
            login_user(new_user, mode)
            return redirect(url_for("home"))
        return render_template('register.html', form=form, current_user='')
    elif mode == 'k':
        form = KorepetytorRegisterForm()
        if form.validate_on_submit():

            # Check if user email is already present in the database.
            result = db.session.execute(db.select(Korepetytor).where(Korepetytor.email == form.email.data))
            user = result.scalar()
            if user:
                # User already exists
                flash("You've already signed up with that email, log in instead!")
                return redirect(url_for('login', mode=mode))

            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = Korepetytor(
                email=form.email.data,
                name=form.name.data,
                surname=form.surname.data,
                password=hash_and_salted_password,
                phone_number=form.phone_number.data,
                bank_acc_num=form.bank_acc_num.data,
            )
            db.session.add(new_user)
            db.session.commit()
            # This line will authenticate the user with Flask-Login
            login_user(new_user, mode)
            return redirect(url_for("home"))
        return render_template('register.html', form=form, current_user='')


@app.route('/login/<mode>', methods=["GET", "POST"])
def login(mode):
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(Uczen).where(Uczen.email == form.email.data))
        if result is None:
            result = db.session.execute(db.select(Korepetytor).where(Korepetytor.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login', mode=mode))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login', mode=mode))
        else:
            login_user(user, mode)
            return redirect(url_for('get_all_posts'))

    return render_template("login.html", form=form, current_user=current_user, mode=mode)


if __name__ == "__main__":
    app.run(debug=True)
