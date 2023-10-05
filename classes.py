from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, ForeignKey, Column, Integer, String, Float, Time, Boolean
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# ------------------------------ tabele dostępnmych dni -----------------------------------  #


class Post(db.Model):
    __tablename__ = "posty"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    subject = Column(String(250), unique=True, nullable=False)
    hours_per_lesson = Column(Float, nullable=False)
    lessons_per_week = Column(Integer, nullable=False)

    # Relacja do dostępności



class Availability(db.Model):
    __tablename__ = "availabilities"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="availabilities")

    days = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sb", "Nd"]
    hours = range(6, 23)
    for day in days:
        for hour in hours:
            locals()[f"{day}_{hour}:00-{hour + 1}:00"] = Column(Boolean)


# ------------------------------ tabele użytkowników -----------------------------------  #

# Tabela asocjacyjna dla relacji many-to-many między Uczen a Korepetytor
association_table = db.Table('korepetytor_uczen',
    db.Column('korepetytor_id', db.String(100), db.ForeignKey('users.id')),
    db.Column('uczen_id', db.String(100), db.ForeignKey('users.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_type = db.Column(db.String(10), nullable=False)  # 'uczen' lub 'korepetytor'
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    bank_acc_num = db.Column(db.String(100), nullable=True)  # tylko dla korepetytor
    email_confirmation_code = db.Column(db.String(100), nullable=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    posts = relationship("Post", back_populates="author") # tylko dla ucznia
    availabilities = relationship("Availability", back_populates="user")

    korepetytorzy = db.relationship(
        "User",
        secondary=association_table,
        primaryjoin=(association_table.c.uczen_id == id),
        secondaryjoin=(association_table.c.korepetytor_id == id),
        backref=db.backref('uczniowie', lazy='dynamic'),
        lazy='dynamic'
    )
