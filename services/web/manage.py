from project.api_struc.models import User, Exercise, Workout, Action, Challenge, UserChallenge
from project import app, db
import project.misc.funcs as funcs
from flask.cli import FlaskGroup
import datetime
from pytz import timezone
import os
from debugger import initialize_flask_server_debugger_if_needed

initialize_flask_server_debugger_if_needed()

cli = FlaskGroup(app)
# app, db = create_app("config")

# enables to run something like "python manage.py create_db", which is used in the Makefile.


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    try:
        user2 = User(
            id=funcs.rand_user_id(),
            email="kantnprojekt@gmail.com",
            user_name="kantnprojekt",
            password="781500543b5461cbdf28f82e3d79a3d9",  # 123456
            token="5tABELThgUIc5oH5j9jbIU2AKedRYa",
        )
        user1 = User(
            id=funcs.rand_user_id(),
            email="joel.gotsch@gmail.com",
            user_name="Viech",
            password="781500543b5461cbdf28f82e3d79a3d9",  # 123456
            token="IJyyJhgSlc4LjNOFmjWOIKZ0iRzQ6Y",)

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        ex1 = Exercise(
            id=funcs.rand_string(30),
            title="Schritte",
            note="Anzahl der Schritte pro Tag. Jeder Schritt zählt 0.01 Punkte.",
            user_id=user1.id,
            points=0.01)
        ex2 = Exercise(
            id=funcs.rand_string(30),
            title="Liegestütze",
            note="Jeder Liegestütz zählt 1 Punkt.",
            user_id=user1.id,
            points=1)
        ex3 = Exercise(
            id=funcs.rand_string(30),
            title="Situps",
            note="Jeder Situp zählt 0.25 Punkte.",
            user_id=user1.id,
            points=0.25)
        ex4 = Exercise(
            id=funcs.rand_string(30),
            title="Klimmzüge",
            note="Jeder Klimmzug zählt 4 Punkte.",
            user_id=user1.id,
            points=4)
        ex5 = Exercise(
            id=funcs.rand_string(30),
            title="Hollow Hold",
            note="Jede Minute im Hollow Hold zählt 20 Punkte.",
            user_id=user1.id,
            unit="min",
            points=20)
        ex6 = Exercise(
            id=funcs.rand_string(30),
            title="Plank",
            note="Alle Versionen sind OK: Front-Plank, Side-Plank,... 15 Punkte pro Minute",
            user_id=user1.id,
            unit="min",
            points=15)
        ex7 = Exercise(
            id=funcs.rand_string(30),
            title="(Wand-) Handstand",
            note="Handstand an der Wand oder freistehend. 25 Punkte pro Minute",
            user_id=user1.id,
            unit="min",
            points=25)
        ex8 = Exercise(
            id=funcs.rand_string(30),
            title="Superman",
            note="Bauch am Boden, Arme nach vorne und Beine hinten in die Luft gestreckt, Hintern anspannen.",
            user_id=user1.id,
            unit="min",
            points=10)
        ex9 = Exercise(
            id=funcs.rand_string(30),
            title="Schlaf",
            note="Jede Stunde Schlaf bringt 10 Punkte. Aber maximal 80 Punkte pro Tag/Nacht.",
            user_id=user1.id,
            unit="h",
            points=10,
            max_points_day=80)
        ex10 = Exercise(
            id=funcs.rand_string(30),
            title="Alkohol",
            note="Für jedes Bier (oder etwa äquivalente Menge Alkohol) gibt es 50 Punkte Abzug. Ein Bier pro Woche ist aber frei.",
            user_id=user1.id,
            unit="Bier",
            points=-50,
            weekly_allowance=1)
        ex11 = Exercise(
            id=funcs.rand_string(30),
            title="Yoga",
            note="Alle Yoga Formen sind OK.",
            user_id=user1.id,
            unit="min",
            points=3)
        # missing: Plank, Wall-Handstand, Superman, Yoga

        challenge1 = Challenge(
            id=funcs.rand_string(30),
            name="Kantnprojekt",
            description="2000 Punkte pro Kalenderwoche müssen erreicht werden. Diese setzen sich aus allen Übungen inklusive Schlaf und abzüglich Alkohol zusammen.",
            min_points=2000,
            eval_period="week",
            start_date=datetime.datetime.utcnow(),
            end_date=datetime.datetime.utcnow()+datetime.timedelta(days=90))
        print("appending all exercises...")
        challenge1.exercises.append(ex1)
        challenge1.exercises.append(ex2)
        challenge1.exercises.append(ex3)
        challenge1.exercises.append(ex4)
        challenge1.exercises.append(ex5)
        challenge1.exercises.append(ex6)
        challenge1.exercises.append(ex7)
        challenge1.exercises.append(ex8)
        challenge1.exercises.append(ex9)
        challenge1.exercises.append(ex10)
        challenge1.exercises.append(ex11)
        accepted_chall_1 = UserChallenge()
        accepted_chall_1.user = user2
        accepted_chall_1.challenge = challenge1

        for ch in user2.challenges:
            print(ch.challenge.name + ":")
            print(" Übungen:")
            for ex in ch.challenge.exercises:
                print("     "+ex.title)
            print(" Teilnehmer:")
            for us in ch.challenge.users:
                print("     "+us.user.user_name)

        print("adding all exercises...")
        db.session.add(ex1)
        db.session.add(ex2)
        db.session.add(ex3)
        db.session.add(ex4)
        db.session.add(ex5)
        db.session.add(ex6)
        db.session.add(ex7)
        db.session.add(ex8)
        db.session.add(ex9)
        db.session.add(ex10)
        db.session.add(ex11)
        print("adding challenge...")
        db.session.add(challenge1)
        print("adding accepted challenge...")
        db.session.add(accepted_chall_1)
        db.session.commit()
        print("adding workouts...")

        wo1 = Workout(
            id=funcs.rand_string(30),
            user_id=user1.id,
            date=datetime.datetime(2020, 9, 21, 15, 0, 0,
                                   tzinfo=timezone('CET')),
            note="Test")
        wo2 = Workout(
            id=funcs.rand_string(30),
            user_id=user1.id,
            date=datetime.datetime(2020, 9, 20, 15, 0, 0,
                                   tzinfo=timezone('CET')),
            note="Test2")
        db.session.add(wo1)
        db.session.add(wo2)
        db.session.commit()
        print("adding actions...")

        ac1 = Action(
            id=funcs.rand_string(30),
            exercise_id=ex6.id, workout_id=wo1.id,
            number=7.5)  # sleep
        ac2 = Action(
            id=funcs.rand_string(30),
            exercise_id=ex1.id, workout_id=wo1.id,
            number=26000)  # steps
        wo1.actions.append(ac1)
        wo1.actions.append(ac2)
        # db.session.add(wo1)
        db.session.commit()
        print(Action.query.get(ac1.id))
        # TODO: test deleting entries
    except Exception as e:
        print(e)


if __name__ == "__main__":
    cli()
