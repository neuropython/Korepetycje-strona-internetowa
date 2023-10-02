from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, SelectMultipleField, FieldList, FormField, TimeField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class AvailabilityForm(FlaskForm):
    day = SelectField('Dzień tygodnia', choices=[
        ('1', 'Poniedziałek'),
        ('2', 'Wtorek'),
        ('3', 'Środa'),
        ('4', 'Czwartek'),
        ('5', 'Piątek'),
        ('6', 'Sobota'),
        ('7', 'Niedziela')
    ], validators=[DataRequired()])
    time_slots = SelectMultipleField('Dostępne godziny', choices=[
        '6-7',
        '7-8',
        '8-9',
        '9-10',
        '10-11',
        '11-12',
        '12-13',
        '13-14',
        '14-15',
        '15-16',
        '16-17',
        '17-18',
        '18-19',
        '19-20',
        '20-21',
        '21-22',
        '22-23',
        '23-24'
    ], validators=[DataRequired()])


class TutoringPostForm(FlaskForm):
    subject = StringField('Przedmiot', validators=[DataRequired()])
    hours_per_lesson = FloatField('Godziny na lekcję', validators=[DataRequired()])
    lessons_per_week = IntegerField('Lekcje na tydzień', validators=[DataRequired()])
    availabilities = FieldList(FormField(AvailabilityForm), label='Dostępność', min_entries=1)
    submit = SubmitField('Dodaj Post')



# Create a RegisterForm to register new users
class UczenRegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
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
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    name = StringField("Imię", validators=[DataRequired()])
    surname = StringField("Nazwisko", validators=[DataRequired()])
    phone_number = StringField("Numer telefonu", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class KorepetytorRegisterForm(FlaskForm):
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
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


# Create a confirm form to confirm users
class ConfirmEmailForm(FlaskForm):
    confirmation_code = StringField("Confirmation Code:", validators=[DataRequired()])
    submit = SubmitField("Submit")

