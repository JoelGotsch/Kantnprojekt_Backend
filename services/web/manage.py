from flask.cli import FlaskGroup
import datetime
import os

# from app import create_app 
print("Folders in current working directory:")
for fd in os.walk(os.getcwd()):
    print(str(fd)+ ", ")
print("Folders in current file env:")
for fd in os.walk(os.path.dirname(os.path.realpath(__file__))):
    print(str(fd)+ ", ")
from project import app, db
from project.api_struc.models import User, Exercise, Workout, Action, Challenge, UserChallenge

cli = FlaskGroup(app)
# app, db = create_app("config")

#enables to run something like "python manage.py create_db", which is used in the docker file.
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    user1 = User(emailadress="kantnprojekt@gmail.com",
                 username="kantnprojekt")
    user2 = User(emailadress="joel.gotsch@gmail.com",  username="Viech")
    ex1 = Exercise(title="Schritte",
                   note="Anzahl der Schritte pro Tag. Jeder Schritt zählt 0.01 Punkte.",
                   user_id=user1.id,
                   points=0.01)
    ex2 = Exercise(title="Liegestütze",
                   note="Jeder Liegestütz zählt 1 Punkt.",
                   user_id=user1.id,
                   points=1)
    ex3 = Exercise(title="Situps",
                   note="Jeder Situp zählt 0.25 Punkte.",
                   user_id=user1.id,
                   points=0.25)
    ex4 = Exercise(title="Klimmzüge",
                   note="Jeder Klimmzug zählt 4 Punkte.",
                   user_id=user1.id,
                   points=4)
    ex5 = Exercise(title="Hollow Hold",
                   note="Jede Minute im Hollow Hold zählt 20 Punkte.",
                   user_id=user1.id,
                   unit="min",
                   points=20)
    ex6 = Exercise(title="Schlaf",
                   note="Jede Stunde Schlaf bringt 10 Punkte. Aber maximal 80 Punkte pro Tag/Nacht.",
                   user_id=user1.id,
                   unit="h",
                   points=10,
                   max_points_day=80)
    ex7 = Exercise(title="Alkohol",
                   note="Für jedes Bier (oder etwa äquivalente Menge Alkohol) gibt es 50 Punkte Abzug. Ein Bier pro Woche ist aber frei.",
                   user_id=user1.id,
                   unit="Bier",
                   points=-50,
                   weekly_allowance=1)
    # missing: Plank, Wall-Handstand, Superman, Yoga

    challenge1 = Challenge(name="Kantnprojekt",
                           description="2000 Punkte pro Kalenderwoche müssen erreicht werden. Diese setzen sich aus allen Übungen inklusive Schlaf und abzüglich Alkohol zusammen.",
                           min_points=2000,
                           eval_period="week",
                           start_date=datetime.datetime.utcnow(),
                           end_date=datetime.datetime.utcnow()+datetime.timedelta(days=90))

    challenge1.exercises.append(ex1)
    challenge1.exercises.append(ex2)
    challenge1.exercises.append(ex3)
    challenge1.exercises.append(ex4)
    challenge1.exercises.append(ex5)
    challenge1.exercises.append(ex6)
    challenge1.exercises.append(ex7)
    accepted_chall_1=UserChallenge()
    accepted_chall_1.user=user2
    accepted_chall_1.challenge=challenge1

    for ch in user2.challenges:
        print(ch.challenge.name+ ":")
        print(" Übungen:")
        for ex in ch.challenge.exercises:
            print("     "+ex.title)
        print(" Teilnehmer:")
        for us in ch.challenge.users:
            print("     "+us.user.username)
        

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(ex1)
    db.session.add(ex2)
    db.session.add(ex3)
    db.session.add(ex4)
    db.session.add(ex5)
    db.session.add(ex6)
    db.session.add(ex7)
    db.session.add(challenge1)
    db.session.add(accepted_chall_1)
    db.session.commit()
    #TODO: test deleting entries


if __name__ == "__main__":
    cli()
