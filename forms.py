from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, SelectMultipleField, FieldList, FormField, TimeField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class AvailabilityForm(FlaskForm):
    days = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sb", "Nd"]
    hours = range(6, 23)

    for day in days:
        for hour in hours:
            locals()[f"{day}_{hour}"] = BooleanField(f"{day} {hour}:00-{hour + 1}:00", default=False)

    submit = SubmitField('Dodaj swoją dostępność')


class TutoringPostForm(FlaskForm):
    subject = StringField('Przedmiot', validators=[DataRequired()])
    hours_per_lesson = FloatField('Godziny na lekcję', validators=[DataRequired()])
    lessons_per_week = IntegerField('Lekcje na tydzień', validators=[DataRequired()])
    # Tutaj mamy listę formularzy dostępności dla każdego postu
    submit = SubmitField('Dodaj Post')


class RegisterForm(FlaskForm):
    who = SelectField('Jestem', choices=['Uczniem', 'Korepetytorem'], validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Nieprawidłowy format adresu email.")])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Hasło musi mieć co najmniej 8 znaków."),
            Regexp(r'(?=.*\d)', message="Hasło musi zawierać co najmniej jedną cyfrę."),
            Regexp(r'(?=.*[A-Z])', message="Hasło musi zawierać co najmniej jedną wielką literę."),
            Regexp(r'(?=.*[a-z])', message="Hasło musi zawierać co najmniej jedną małą literę."),
            Regexp(r'(?=.*[!@#$%^&*])', message="Hasło musi zawierać co najmniej jeden ze znaków specjalnych (!@#$%^&*).")
        ]
    )
    confirm_password = PasswordField("Potwierdź hasło", validators=[DataRequired(), EqualTo('password', message='Hasła muszą się zgadzać.')])
    name = StringField("Imię", validators=[DataRequired()])
    surname = StringField("Nazwisko", validators=[DataRequired()])
    phone_number = StringField("Numer telefonu", validators=[DataRequired()])
    bank_acc_num = StringField("Numer konta bankowego", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


# Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    who = SelectField('Jestem', choices=['Uczniem', 'Korepetytorem'], validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


# Create a confirm form to confirm users
class ConfirmEmailForm(FlaskForm):
    confirmation_code = StringField("Confirmation Code:", validators=[DataRequired()])
    submit = SubmitField("Submit")

