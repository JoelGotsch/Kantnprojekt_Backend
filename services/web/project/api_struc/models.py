# from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from datetime import datetime
# from app import db
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()

def default_username(context):
    return context.get_current_parameters()['emailadress']

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    emailadress = db.Column(db.String(), unique=True)
    username = db.Column(db.String(), default=default_username, unique=True)
    firstname = db.Column(db.String(), default="")
    lastname = db.Column(db.String(), default="")
    password = db.Column(db.String(), default="")
    api_key = db.Column(db.String(), default="")
    challenges = db.relationship("UserChallenge", back_populates="user")

    def __repr__(self):
        return('<id {}>'.format(self.id))

    def serialize(self):
        return({
            'api_key' : self.api_key,
            'id' : self.id,
            'username' : self.username,
            'firstname' : self.firstname,
            'lastname' : self.lastname,
            'password' : self.password,
            'emailadress' : self.emailadress,
        })

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    note = db.Column(db.String(), default="")
    # completed = db.Column(db.Boolean(), default=False, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))# user which created that exercise
    unit = db.Column(db.String(), default="")
    points = db.Column(db.Float(), default=0)
    max_points_day = db.Column(db.Float(), default=0)
    weekly_allowance = db.Column(db.Float(), default=0)
    
    def __repr__(self):
        return('<id {}>'.format(self.id))

    def serialize(self):
        return ({
            'title' : self.title,
            'user_id' : self.user_id,
            'note' : self.note,
            'unit' : self.unit,
            'points' : self.points,
            'max_points_day' : self.max_points_day,
            'weekly_allowance' : self.weekly_allowance,
            'id' : self.id,
        })



class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())# user which did the workout
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    note = db.Column(db.String(), default="")

    def __repr__(self):
        return('<id {}>'.format(self.id))

    def serialize(self):
        return ({
            'user_id' : self.user_id,
            'date' : self.date,
            'note' : self.note,
            'id' : self.id,
        })

class Action(db.Model):
    __tablename__ = 'actions'
    # 
    id = db.Column(db.Integer(), primary_key=True)
    execercise_id = db.Column(db.Integer(), db.ForeignKey("exercises.id"))
    workout_id = db.Column(db.Integer(), db.ForeignKey("workouts.id"))
    number = db.Column(db.Integer())
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    note = db.Column(db.String(), default="")

    def __init__(self, date=datetime.today(), note=""):
        self.date = date
        self.note = note

    def __repr__(self):
        return('<id {}>'.format(self.id))

    def serialize(self):
        return ({
            'date' : self.date,
            'note' : self.note,
            'id' : self.id,
        })

# as a challenge contains multiple exercises and an exercise can be part of many challenges, we have a many-to-many relationship here.
# so we implement like suggeste here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
#lets check if db.Integer works without () at the end
challenge_exercises = db.Table('challenge_exercises',
    db.Column('challenge_id', db.Integer(), db.ForeignKey('challenges.id'), primary_key=True),
    db.Column('exercise_id', db.Integer(), db.ForeignKey('exercises.id'), primary_key=True)
)

class Challenge(db.Model):
    __tablename__ = 'challenges'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())
    exercises = db.relationship('Exercise', secondary=challenge_exercises, lazy='subquery',
        backref=db.backref('challenges', lazy=True))
    users = db.relationship("UserChallenge", back_populates="challenge")
    # users = db.relationship('User', secondary='user_challenges', lazy='subquery',
    #     backref=db.backref('challenges', lazy=True))
    # user_challenges = db.relationship('UserChallenge', secondary="user_challenges")
    min_points = db.Column(db.Float())
    eval_period = db.Column(db.String())
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())

    def __repr__(self):
        return('<id {}>'.format(self.id))

    def serialize(self):
        return ({
            'date' : self.date,
            'note' : self.note,
            'user_id' : self.user_id,
            'id' : self.id,
        })

# in this case we implement like described in the documentation for SQLAlchemy v1.3 (which is also valid for 1.4): https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#association-pattern
class UserChallenge(db.Model):
    __tablename__ = 'user_challenges'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    challenge_id = db.Column(db.Integer(), db.ForeignKey('challenges.id'), primary_key=True)
    user_start_challenge = db.Column(db.DateTime(), default=datetime.utcnow())
    user = db.relationship('User', back_populates="challenges") # if user is deleted, his association to challenges should be deleted too. However, we don't want to delete the user if he drops out of a challenge ;)
    challenge = db.relationship('Challenge', back_populates="users")