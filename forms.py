from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    subject = StringField("Blog Post Title", validators=[DataRequired()])
    hours_per_lesson = StringField("Subtitle", validators=[DataRequired()])
    lessons_per_week = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    weekday = CKEditorField("Blog Content", validators=[DataRequired()])
    hours = SubmitField("Submit Post")



# Create a RegisterForm to register new users
class UczenRegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Imię", validators=[DataRequired()])
    surname = StringField("Nazwisko", validators=[DataRequired()])
    phone_number = StringField("Numer telefonu", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class KorepetytorRegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Imię", validators=[DataRequired()])
    surname = StringField("Nazwisko", validators=[DataRequired()])
    phone_number = StringField("Numer telefonu", validators=[DataRequired()])
    bank_acc_num = StringField("Numer konta bankowego", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


# Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


# Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    comment = CKEditorField("Comment")
    submit = SubmitField("Send comment")
