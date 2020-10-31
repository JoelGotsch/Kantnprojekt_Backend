# from flask import Flask
import random
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from datetime import datetime
# from app import db
from flask_sqlalchemy import SQLAlchemy

from ..misc import funcs as funcs

ma = Marshmallow()
db = SQLAlchemy()


def default_user_name(context):
    return context.get_current_parameters()['email']


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(), unique=True)
    user_name = db.Column(db.String(), default=default_user_name, unique=True)
    password = db.Column(db.String(), default="")
    token = db.Column(db.String(30), default=funcs.rand_string(30))
    date_creation = db.Column(
        db.DateTime(), default=datetime.utcnow())
    date_last_login = db.Column(
        db.DateTime(), default=datetime.utcnow())
    challenges = db.relationship("UserChallenge", back_populates="user")

    def __repr__(self):
        return('<user_id {}>'.format(self.id))

    def serialize(self):
        return({
            'token': self.token,
            'user_id': self.id,
            'user_name': self.user_name,
            'email': self.email,
        })


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.String(), primary_key=True,
                   default=funcs.rand_string(30))
    title = db.Column(db.String())
    note = db.Column(db.String(), default="")
    # completed = db.Column(db.Boolean(), default=False, nullable=False)
    # user which created that exercise
    user_id = db.Column(db.String(), db.ForeignKey("users.id"))
    unit = db.Column(db.String(), default="")
    points = db.Column(db.Float(), default=0)
    max_points_day = db.Column(db.Float(), default=0)
    weekly_allowance = db.Column(db.Integer(), default=0)
    not_deleted = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return('<id {}>'.format(self.id))

    def serialize(self):
        return ({
            'id': self.id,
            'title': self.title,
            'user_id': self.user_id,
            'note': self.note,
            'unit': self.unit,
            'points': self.points,
            'max_points_day': self.max_points_day,
            'weekly_allowance': self.weekly_allowance,
            'not_deleted': self.not_deleted,
        })


class Action(db.Model):
    __tablename__ = 'actions'
    #
    id = db.Column(db.String(), primary_key=True,
                   default=funcs.rand_string(30))
    exercise_id = db.Column(db.String(), db.ForeignKey("exercises.id"))
    workout_id = db.Column(db.String(), db.ForeignKey("workouts.id"))
    number = db.Column(db.Integer())
    note = db.Column(db.String(), default="")
    # def __init__(self, note=""):
    #     self.note = note

    def __repr__(self):
        return('<id {}>'.format(self.id))

    def get_points(self):
        return(Exercise.query.get(self.exercise_id).points * self.number)

    def serialize(self):
        return ({
            'id': self.id,
            'exercise_id': self.exercise_id,
            'workout_id': self.workout_id,
            'exercise': Exercise.query.get(self.exercise_id).serialize(),
            'number': self.number,
            'note': self.note,
            'points': self.get_points(),
        })


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.String(), primary_key=True,
                   default=funcs.rand_string(30))
    user_id = db.Column(db.String())  # user which did the workout
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    note = db.Column(db.String(), default="")
    actions = db.relationship('Action', backref=db.backref('workout', lazy=True))
    latest_edit = db.Column(db.DateTime(), default=datetime.utcnow())
    not_deleted = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        return('<id {}>'.format(self.id))

    def serialize(self):
        return ({
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'note': self.note,
            'points': sum([ac.get_points() for ac in self.actions]),
            'actions': {action.id: action.serialize() for action in self.actions},
            'not_deleted': self.not_deleted,
            'latest_edit': self.latest_edit.isoformat(),
        })



# as a challenge contains multiple exercises and an exercise can be part of many challenges, we have a many-to-many relationship here.
# so we implement like suggeste here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
challenge_exercises = db.Table('challenge_exercises',
                               db.Column('challenge_id', db.String(), db.ForeignKey(
                                   'challenges.id'), primary_key=True),
                               db.Column('exercise_id', db.String(), db.ForeignKey(
                                   'exercises.id'), primary_key=True)
                               )


class Challenge(db.Model):
    __tablename__ = 'challenges'

    id = db.Column(db.String(), primary_key=True,
                   default=funcs.rand_string(30))
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
            'date': self.date,
            'note': self.note,
            'user_id': self.user_id,
            'id': self.id,
        })

# in this case we implement like described in the documentation for SQLAlchemy v1.3 (which is also valid for 1.4): https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#association-pattern


class UserChallenge(db.Model):
    __tablename__ = 'user_challenges'
    user_id = db.Column(db.String(), db.ForeignKey(
        'users.id'), primary_key=True)
    challenge_id = db.Column(db.String(), db.ForeignKey(
        'challenges.id'), primary_key=True)
    user_start_challenge = db.Column(db.DateTime(), default=datetime.utcnow())
    # if user is deleted, his association to challenges should be deleted too. However, we don't want to delete the user if he drops out of a challenge ;)
    user = db.relationship('User', back_populates="challenges")
    challenge = db.relationship('Challenge', back_populates="users")
