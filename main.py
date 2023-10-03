from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import TutoringPostForm, AvailabilityForm, LoginForm, RegisterForm, ConfirmEmailForm
from classes import db, Post, User, Availability
from datetime import timedelta, datetime
from flask_mail import Mail, Message
import random
import os

# --------------------------------------------------------------- setup -------------------------------------------- #

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_DEFAULT_SENDER'] = os.environ['koreo_mail']
app.config['MAIL_USERNAME'] = os.environ['koreo_mail']
app.config['MAIL_PASSWORD'] = os.environ['koreo_password']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

app.config['SECRET_KEY'] = os.environ['FLASK_KEY']
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


# ----------------------------------------------------------------- funkcje ---------------------------------------- #

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Musisz się zalogować, aby uzyskać dostęp do tej strony!", "danger")
                return redirect(url_for('login'))

            if current_user.user_type != role or not current_user.email_confirmed:
                flash("Dostęp ograniczony!", "warning")
                return redirect(url_for('main'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.context_processor
def inject_user():
    """Automatycznie wstrzykuj 'current_user' do wszystkich szablonów."""
    return {'current_user': current_user}

# ---------------------------------------------- sekcja ucznia ----------------------------------- #


@app.route('/uczen')
@role_required('u')
def uczen():
    return render_template("uczen.html")


@app.route('/add_post', methods=["GET", "POST"])
@role_required('u')
def add():
    form = TutoringPostForm()
    if form.validate_on_submit():
        post = Post(
            author_id=current_user.id,
            subject=form.subject.data,
            hours_per_lesson=form.hours_per_lesson.data,
            lessons_per_week=form.lessons_per_week.data
        )
        db.session.add(post)
        db.session.commit()

        # zbieranie dostępności z formularza
        for day in range(1, 8):
            for hour in range(6, 22):
                availability_value = request.form.get(f'availabilities-{day}-{hour}', '0')
                if availability_value == '1':
                    availability = Availability(
                        day_id=day,
                        time_slot=f"{hour}- {hour+1}",
                        post=post
                    )
                    db.session.add(availability)

        db.session.commit()
        return redirect(url_for('uczen'))

    return render_template('add.html', form=form)


@app.route('/my_posts')
@role_required('u')
def posts():
    return render_template("posts.html")


# ---------------------------------------------- sekcja korepetytora ------------------------------ #


@app.route('/korepetytor')
@role_required('k')
def korepetytor():
    return render_template('korepetytor.html')


@app.route('/all_posts')
@role_required('k')
def all_posts():
    return render_template('all_posts.html')


@app.route('/my_clients')
@role_required('k')
def clients():
    return render_template('clients.html')


# ----------------------------------------------- inne ---------------------------------------- #
@app.route('/availability', methods=["GET", "POST"])
def add_availability():
    if not current_user.is_authenticated:
        flash("Musisz być zalogowany, aby ustawić dostępność!", "error")
        return redirect(url_for('login'))

    form = AvailabilityForm()

    if request.method == "GET":
        current_availability = Availability.query.filter_by(user_id=current_user.id).first()
        if current_availability:
            for day in form.days:
                for hour in form.hours:
                    getattr(form, f"{day}_{hour}").data = getattr(current_availability,
                                                                  f"{day}_{hour}:00-{hour + 1}:00")

    if form.validate_on_submit():
        # usuń wcześniejsze dostępności dla tego użytkownika
        previous_availability = Availability.query.filter_by(user_id=current_user.id).all()
        for avail in previous_availability:
            db.session.delete(avail)

        new_availability = Availability(user_id=current_user.id)
        # dodaj nowe dostępności
        for day in form.days:
            for hour in form.hours:
                setattr(new_availability, f"{day}_{hour}:00-{hour + 1}:00", getattr(form, f"{day}_{hour}").data)

        db.session.add(new_availability)
        db.session.commit()
        flash("Dostępność została zaktualizowana!", "success")
        return redirect(url_for('uczen' if current_user.user_type == 'u' else 'korepetytor'))

    return render_template('add_availability.html', form=form)


# ----------------------------------------------- logowanie ---------------------------------------- #

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login',))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        confirmation_code = str(random.randint(100000, 999999))
        mode = 'u' if form.who.data == 'Uczniem' else 'k'
        new_user = User(
            user_type=mode,
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            password=hash_and_salted_password,
            phone_number=form.phone_number.data,
            bank_acc_num=form.bank_acc_num.data,
            email_confirmation_code=confirmation_code

        )

        db.session.add(new_user)
        db.session.commit()

        confirmation_url = url_for("confirm_email", user_id=f"{new_user.id}", _external=True)
        msg = Message("Please confirm your email", recipients=[form.email.data])
        msg.body = f"Your confirmation code is: {confirmation_code}\n\nClick the link below to confirm your email:\n{confirmation_url}"
        mail.send(msg)

        flash("Confirmation code has been sent to your email.")
        return redirect(url_for("confirm_email", user_id=f"{new_user.id}"))

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif check_password_hash(user.password, form.password.data):
            if not user.email_confirmed:
                flash("Please confirm your email before logging in.")
                return redirect(url_for("confirm_email", user_id=f"{user.id}"))

            login_user(user)
            mode = form.who.data
            return redirect(url_for('uczen' if mode == 'u' else 'korepetytor'))
        else:
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))

    return render_template("login.html", form=form)


@app.route('/confirm-email/<user_id>', methods=["GET", "POST"])
def confirm_email(user_id):
    user = load_user(user_id)
    if not user:
        abort(404)
    form = ConfirmEmailForm()

    if form.validate_on_submit():
        code = form.confirmation_code.data

        if user.email_confirmation_code == code:
            user.email_confirmed = True
            db.session.commit()
            login_user(user)
            return redirect(url_for('uczen' if user.user_type == 'u' else 'korepetytor'))
        else:
            flash("Invalid confirmation code. Try again.", "danger")

    return render_template('confirm_email.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
