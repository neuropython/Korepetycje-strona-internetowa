from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


db = SQLAlchemy()

# CONFIGURE TABLES
class Post(db.Model):
    __tablename__ = "posty"
    id = db.Column(db.Integer, primary_key=True)

    #Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("uczniowie.id"))
    #Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    author = relationship("Uczen", back_populates="posts")

    subject = db.Column(db.String(250), unique=True, nullable=False)
    hours_per_lesson = db.Column(db.Float, nullable=False)
    lessons_per_week = db.Column(db.Integer, nullable=False)
    weekday = db.Column(db.String(250), nullable=False)
    hours = db.Column(db.Text, nullable=False)


class Uczen(UserMixin, db.Model):
    __tablename__ = "uczniowie"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    #This will act like a List of BlogPost objects attached to each User.
    #The "author" refers to the author property in the BlogPost class.
    posts = relationship("Post", back_populates="author")

    teacher_id = db.Column(db.Integer, db.ForeignKey("korepetytorzy.id"))
    teacher = relationship("Uczen", back_populates="students")


class Korepetytor(UserMixin, db.Model):
    __tablename__ = "korepetytorzy"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    bank_acc_num = db.Column(db.String(100))

    students = relationship("Uczen", back_populates="teacher")



