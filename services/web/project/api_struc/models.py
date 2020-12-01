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

    id = db.Column(db.String(30), primary_key=True, default=funcs.rand_string)
    email = db.Column(db.String(), unique=True)
    user_name = db.Column(db.String(), default=default_user_name, unique=True)
    password = db.Column(db.String(), default="")
    exercises = db.relationship("UserExercise", back_populates="user")
    token = db.Column(db.String(30), default=funcs.rand_string)
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

    id = db.Column(db.String(), primary_key=True, default=funcs.rand_string)
    title = db.Column(db.String())
    note = db.Column(db.String(), default="")
    description = db.Column(db.String(), default="")
    # completed = db.Column(db.Boolean(), default=False, nullable=False)
    # user which created that exercise
    user_id = db.Column(db.String(), db.ForeignKey("users.id"))
    unit = db.Column(db.String(), default="")
    points = db.Column(db.Float(), default=0)
    max_points_day = db.Column(db.Float(), default=0)
    max_points_week = db.Column(db.Float(), default=0)
    daily_allowance = db.Column(db.Float(), default=0)
    weekly_allowance = db.Column(db.Float(), default=0)
    checkbox = db.Column(db.Boolean(), default=False) #not yet used, but here for future feature: Exercises which you do on a regular basis, but max 1 per day/week/..
    checkbox_reset = db.Column(db.Integer(), default=2) #1 = per reset checkbox per workout, 2 = reset per day, 3 = reset per week, 4 = reset per month
    latest_edit = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return('<id {}>'.format(self.id))

    def serialize(self):
        return ({
            'id': self.id,
            'title': self.title,
            'user_id': self.user_id,
            'note': self.note,
            'description': self.description,
            'unit': self.unit,
            'points': self.points, # points per unit
            'max_points_day': self.max_points_day,
            'max_points_week': self.max_points_week,
            'daily_allowance': self.daily_allowance,
            'weekly_allowance': self.weekly_allowance,
            'latest_edit': self.latest_edit.isoformat(),
            'checkbox': self.checkbox,
            'checkbox_reset': self.checkbox_reset,
        })

class UserExercise(db.Model):
    __tablename__ = 'user_exercises'

    id = db.Column(db.String(), primary_key=True, default=funcs.rand_string)
    note = db.Column(db.String(), default="")
    exercise_id = db.Column(db.String(), db.ForeignKey("exercises.id"))
    # user which created that exercise
    user_id = db.Column(db.String(), db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="exercises")
    points = db.Column(db.Float(), default=0)
    max_points_day = db.Column(db.Float(), default=0)
    max_points_week = db.Column(db.Float(), default=0)
    daily_allowance = db.Column(db.Float(), default=0)
    weekly_allowance = db.Column(db.Float(), default=0)
    latest_edit = db.Column(db.DateTime(), default=datetime.utcnow)
    private = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return('<id {}>'.format(self.id))

    def serialize(self):
        return ({
            'id': self.id,
            'user_id': self.user_id,
            'note': self.note,
            'exercise_id': self.exercise_id,
            'points': self.points,
            'max_points_day': self.max_points_day,
            'max_points_week': self.max_points_week,
            'daily_allowance': self.daily_allowance,
            'weekly_allowance': self.weekly_allowance,
            'latest_edit': self.latest_edit.isoformat(),
            'private': self.private,
        })

    @property
    def title(self):
        return(Exercise.query.get(self.exercise_id).title)

class ChallengeExercise(db.Model):
    __tablename__ = 'challenge_exercises'

    id = db.Column(db.String(), primary_key=True, default=funcs.rand_string)
    note = db.Column(db.String(), default="")
    exercise_id = db.Column(db.String(), db.ForeignKey("exercises.id"))
    challenge_id = db.Column(db.String(), db.ForeignKey("challenges.id"))
    challenge = db.relationship("Challenge", back_populates="exercises")
    points = db.Column(db.Float(), default=0)
    max_points_day = db.Column(db.Float(), default=0)
    max_points_week = db.Column(db.Float(), default=0)
    daily_allowance = db.Column(db.Float(), default=0)
    weekly_allowance = db.Column(db.Float(), default=0)
    latest_edit = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return('<id {}>'.format(self.id))

    def serialize(self):
        return ({
            'id': self.id,
            'challenge_id': self.challenge.id,
            'note': self.note,
            'exercise_id': self.exercise_id,
            'points': self.points,
            'max_points_day': self.max_points_day,
            'max_points_week': self.max_points_week,
            'daily_allowance': self.daily_allowance,
            'weekly_allowance': self.weekly_allowance,
            'latest_edit': self.latest_edit.isoformat(),
        })

    @property
    def title(self):
        return(Exercise.query.get(self.exercise_id).title)


class Action(db.Model):
    __tablename__ = 'actions'
    #
    id = db.Column(db.String(), primary_key=True,
                   default=funcs.rand_string)
    exercise_id = db.Column(db.String(), db.ForeignKey("exercises.id"))
    workout_id = db.Column(db.String(), db.ForeignKey("workouts.id"))
    number = db.Column(db.Float())
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
                   default=funcs.rand_string)
    user_id = db.Column(db.String())  # user which did the workout
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    note = db.Column(db.String(), default="")
    actions = db.relationship('Action', backref=db.backref('workout', lazy=True))
    latest_edit = db.Column(db.DateTime(), default=datetime.utcnow)

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
            'latest_edit': self.latest_edit.isoformat(),
        })


# now doing it differently: for each challenge, we create ChallengeExercises which are only part of one challenge. The ChallengeExercise then references back to an Exercise.
# # as a challenge contains multiple exercises and an exercise can be part of many challenges, we have a many-to-many relationship here.
# # so we implement like suggeste here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# challenge_exercises = db.Table('challenge_exercises',
#                                db.Column('challenge_id', db.String(), db.ForeignKey(
#                                    'challenges.id'), primary_key=True),
#                                db.Column('exercise_id', db.String(), db.ForeignKey(
#                                    'challenge_exercises.id'), primary_key=True)
#                                )


class Challenge(db.Model):
    __tablename__ = 'challenges'

    id = db.Column(db.String(), primary_key=True,
                   default=funcs.rand_string)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())
    # exercises = db.relationship('ChallengeExercise', secondary=challenge_exercises, lazy='subquery',
    #                             backref=db.backref('challenges', lazy=True))
    exercises = db.relationship("ChallengeExercise", back_populates="challenge")
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
