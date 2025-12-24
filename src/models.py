from flask_sqlalchemy import SQLAlchemy
from db import db

# initializing the postgres database
# importing from db.py so its unified


# creating the users class
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    weight_lbs = db.Column(db.Numeric)
    height_ft = db.Column(db.Numeric)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))

    # a user has many sessions
    sessions = db.relationship('Session', backref='user', lazy=True)


# creating the sessions class
class Session(db.Model):
    __tablename__ = 'sessions'

    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    session_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    duration_mins = db.Column(db.Integer)
    session_type = db.Column(db.String(50), nullable=False)
    muscle_group = db.Column(db.String(50), nullable=False)

    # a session has workouts
    workouts = db.relationship('Workout', backref='session', lazy=True)

# creating the workouts class
class Workout(db.Model):
    __tablename__ = 'workouts'

    workout_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.session_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    exercise_name = db.Column(db.String(100), nullable=False)
    num_sets = db.Column(db.Integer)
    num_reps = db.Column(db.Integer)
    weight_lbs = db.Column(db.Numeric)
    muscle = db.Column(db.String(50), nullable=False)