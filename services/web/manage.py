 # coding=utf-8
from flask_sqlalchemy import SQLAlchemy
from project.api_struc.models import User, Exercise, Workout, Action, Challenge, UserChallenge, UserExercise, ChallengeExercise
from project import app, db
from project.misc.funcs import rand_string, rand_user_id
# from flask.cli import FlaskGroup
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import datetime
from pytz import timezone
import os
from debugger import initialize_flask_server_debugger_if_needed

initialize_flask_server_debugger_if_needed()

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


# cli = FlaskGroup(app)
# app, db = create_app("config")

# enables to run something like "python manage.py create_db", which is used in the Makefile.

def result_dict(r):
    return dict(zip(r.keys(), r))

def result_dicts(rs): 
    return list(map(result_dict, rs))


# @cli.command("print_user")
@manager.command
def start():
    db.create_all()

@manager.command
def print_user():
    result = result_dicts(User.query.all())
    print(result)

@manager.command
def print_workouts():
    result = result_dicts(Workout.query.all())
    print(result)
    

@manager.command
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def backup_dump():
    # print(os.listdir()): If run from VS Code debugger, we are in /home/Kantnprojekt_Backend
    import pathlib
    manage_path = pathlib.Path(__file__).parent.absolute()
    print(manage_path)
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M.dump")
    full_file = os.path.join(manage_path, "project", "backups", filename)
    os.makedirs(full_file, exist_ok = True)
    # see https://stackoverflow.com/questions/4256107/running-bash-commands-in-python/51950538#51950538 for ultimate explenation of subprocess and bash commands
    bashCommand = "export PGPASSWORD='password'; pg_dump -U kantn --host=localhost -d kantnprojekt > "+full_file
    import subprocess
    output = subprocess.run(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, check=True, text = True)
    print(output.stdout)
    print(output.stderr)


@manager.command
def restore_backup_dump(filename=""):
    create_db() # first resetting the tables, then load the data
    import pathlib
    manage_path = pathlib.Path(__file__).parent.absolute()
    backup_path = os.path.join(manage_path, "project", "backups")
    if filename == "":
        # try to get most up-to-date file in backups:
        dirFiles = os.listdir(backup_path) #list of directory files
        dirFiles.sort(reverse=True)
        if len(dirFiles) == 0:
            print("No backup-files found.")
            return
        filename = dirFiles[0]
    full_file = os.path.join(backup_path, filename)
    # bashCommand = "export PGPASSWORD='password'; psql -U kantn --host=localhost -d kantnprojekt < kantnprojekt /home/Kantnprojekt_Backend/services/web/project/backups/"+filename
    bashCommand = "export PGPASSWORD='password'; psql -U kantn --host=localhost -d kantnprojekt < " + full_file
    import subprocess
    import time
    # For some reason, pg_restore and 
    for i in range(6):
        try:
            output = subprocess.run(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=False, text = True)
        except Exception as e:
            print(e)
        time.sleep(0.1)
        print(i)

@manager.command
def backup_dump_docker():
    # print(os.listdir()): If run from VS Code debugger, we are in /home/Kantnprojekt_Backend
    import pathlib
    manage_path = pathlib.Path(__file__).parent.absolute()
    print(manage_path)
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M.dump")
    full_file = os.path.join(manage_path, "project", "backups", filename)
    os.makedirs(full_file, exist_ok = True)
    # see https://stackoverflow.com/questions/4256107/running-bash-commands-in-python/51950538#51950538 for ultimate explenation of subprocess and bash commands
    bashCommand = "export PGPASSWORD='password'; pg_dump -U kantn --host=kantnprojekt_backend_postgres_1 -d kantnprojekt_db > "+full_file
    import subprocess
    output = subprocess.run(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, check=True, text = True)
    print(output.stdout)
    print(output.stderr)


@manager.command
def restore_backup_dump_docker(filename=""):
    import pathlib
    manage_path = pathlib.Path(__file__).parent.absolute()
    backup_path = os.path.join(manage_path, "project", "backups")
    if filename == "":
        # try to get most up-to-date file in backups:
        dirFiles = os.listdir(backup_path) #list of directory files
        dirFiles.sort(reverse=True)
        if len(dirFiles) == 0:
            print("No backup-files found.")
            return
        filename = dirFiles[0]
    full_file = os.path.join(backup_path, filename)
    # bashCommand = "export PGPASSWORD='password'; psql -U kantn --host=localhost -d kantnprojekt < kantnprojekt /home/Kantnprojekt_Backend/services/web/project/backups/"+filename
    bashCommand = "export PGPASSWORD='password'; psql -U kantn --host=kantnprojekt_backend_postgres_1 -d kantnprojekt_db < " + full_file
    import subprocess
    import time
    # For some reason, pg_restore and 
    for i in range(6):
        try:
            output = subprocess.run(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=False, text = True)
        except Exception as e:
            print(e)
        time.sleep(0.1)
        print(i)
        # print(output.stdout)
    # subprocess.check_output()

# Using the binary-commands would be the cleaner choice and should work, but it doesn't. Here it does: https://www.youtube.com/watch?v=nbnRibO5Qmo
# @manager.command
# def backup_dump_binary():
#     # print(os.listdir()): If run from VS Code debugger, we are in /home/Kantnprojekt_Backend
#     os.makedirs("/home/Kantnprojekt_Backend/services/web/project/binary_backups", exist_ok = True)
#     filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M.dump")
#     # see https://stackoverflow.com/questions/4256107/running-bash-commands-in-python/51950538#51950538 for ultimate explenation of subprocess and bash commands
#     bashCommand = "export PGPASSWORD='password'; pg_dump -Fc -U kantn --host=localhost -d kantnprojekt > /home/Kantnprojekt_Backend/services/web/project/binary_backups/"+filename
#     import subprocess
#     output = subprocess.run(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True, check=True, text = True)
#     print(output.stdout)
#     print(output.stderr)

# @manager.command
# def restore_backup_dump_binary(filename=""):
#     create_db() # first resetting the tables, then load the data
#     if filename == "":
#         # try to get most up-to-date file in backups:
#         dirFiles = os.listdir('/home/Kantnprojekt_Backend/services/web/project/binary_backups') #list of directory files
#         dirFiles.sort(reverse=True)
#         if len(dirFiles) == 0:
#             print("No backup-files found.")
#             return
#         filename = dirFiles[0]

#     # bashCommand = "export PGPASSWORD='password'; psql -U kantn --host=localhost -d kantnprojekt < kantnprojekt /home/Kantnprojekt_Backend/services/web/project/backups/"+filename
#     bashCommand = "export PGPASSWORD='password'; pg_restore -U kantn --host=localhost -d kantnprojekt /home/Kantnprojekt_Backend/services/web/project/binary_backups/"+filename
#     import subprocess
#     output = subprocess.run(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=False, text = True)
#     print(output.stdout)
#     # subprocess.check_output()
@manager.command
def delete_wallsits():
    # check if user-exercises where deleted also (it should be!)
    # db.session.commit()
    try:
        wallsit_exs = Exercise.query.filter(Exercise.title == "Wallsit").all()
        wallsit_us_exs = [UserExercise.query.filter(UserExercise.exercise_id == ex.id).first() for ex in wallsit_exs]
        wallsit_actions = [Action.query.filter(Action.exercise_id == ex.id).first() for ex in wallsit_exs]

        for ac in wallsit_actions:
            if ac is not None:
                wo = Workout.query.get(ac.workout_id)
                wo.latest_edit = datetime.datetime.now()
                db.session.delete(ac)
        db.session.commit()
        
        for us_ex in wallsit_us_exs:
            if us_ex is not None:
                db.session.delete(us_ex)
        db.session.commit()
        
        for ex in wallsit_exs:
            if ex is not None:
                db.session.delete(ex)
        db.session.commit()
    except Exception as e:
        print("Exception was expected...")
        print(e)

@manager.command
def create_admin_exercises():
    try:
        admin_user = User.query.filter_by(
                        user_name="kantnprojekt").first()
        my_user =  User.query.filter_by(
                        user_name="Viech").first()
        for us_ex in my_user.exercises:
            # check if admin_user has exercise with 
            exercise_id = us_ex.exercise_id
            admin_has_ex = False
            for ad_us_ex in admin_user.exercises:
                if ad_us_ex.id == exercise_id:
                    admin_has_ex = True
            if not admin_has_ex:
                exercise = Exercise.query.get(us_ex.exercise_id)
                new_ad_us_ex = UserExercise(
                            note=exercise.note,
                            exercise_id=exercise.id,
                            user_id=admin_user.id,
                            user=admin_user,
                            points=exercise.points,
                            max_points_day=exercise.max_points_day,
                            max_points_week=exercise.max_points_week,
                            daily_allowance=exercise.daily_allowance,
                            weekly_allowance=exercise.weekly_allowance,
                        )
                db.session.add(new_ad_us_ex)
                db.session.commit()
    except Exception as e:
        print("Exception was expected...")
        print(e)


@manager.command
def seed_db():
    try:
        user1= User(
            id=rand_user_id(),
            email="kantnprojekt@gmail.com",
            user_name="kantnprojekt",
            password="781500543b5461cbdf28f82e3d79a3d9",  # 123456
            token="5tABELThgUIc5oH5j9jbIU2AKedRYa",
        )
        user2 = User(
            id=rand_user_id(),
            email="joel.gotsch@gmail.com",
            user_name="Viech",
            password="781500543b5461cbdf28f82e3d79a3d9",  # 123456
            token="IJyyJhgSlc4LjNOFmjWOIKZ0iRzQ6Y",)

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        ex1 = Exercise(
            id=rand_string(30),
            title="Schritte",
            note="Anzahl der Schritte pro Tag. Jeder Schritt zählt 0.01 Punkte.",
            user_id=user1.id,
            points=0.01)
        ex2 = Exercise(
            id=rand_string(30),
            title="Liegestütze",
            note="Jeder Liegestütz zählt 1 Punkt.",
            user_id=user1.id,
            points=1)
        ex3 = Exercise(
            id=rand_string(30),
            title="Situps",
            note="Jeder Situp zählt 0.25 Punkte.",
            user_id=user1.id,
            points=0.25)
        ex4 = Exercise(
            id=rand_string(30),
            title="Klimmzüge",
            note="Jeder Klimmzug zählt 4 Punkte.",
            user_id=user1.id,
            points=4)
        ex5 = Exercise(
            id=rand_string(30),
            title="Hollow Hold",
            note="Jede Minute im Hollow Hold zählt 20 Punkte.",
            user_id=user1.id,
            unit="min",
            points=20)
        ex6 = Exercise(
            id=rand_string(30),
            title="Plank",
            note="Alle Versionen sind OK: Front-Plank, Side-Plank,... 15 Punkte pro Minute",
            user_id=user1.id,
            unit="min",
            points=15)
        ex7 = Exercise(
            id=rand_string(30),
            title="(Wand-) Handstand",
            note="Handstand an der Wand oder freistehend. 25 Punkte pro Minute",
            user_id=user1.id,
            unit="min",
            points=25)
        ex8 = Exercise(
            id=rand_string(30),
            title="Superman",
            note="Bauch am Boden, Arme nach vorne und Beine hinten in die Luft gestreckt, Hintern anspannen.",
            user_id=user1.id,
            unit="min",
            points=10)
        ex9 = Exercise(
            id=rand_string(30),
            title="Schlaf",
            note="Jede Stunde Schlaf bringt 10 Punkte. Aber maximal 80 Punkte pro Tag/Nacht.",
            user_id=user1.id,
            unit="h",
            points=10,
            max_points_day=80)
        ex10 = Exercise(
            id=rand_string(30),
            title="Alkohol",
            note="Für jedes Bier (oder etwa äquivalente Menge Alkohol) gibt es 50 Punkte Abzug. Ein Bier pro Woche ist aber frei.",
            user_id=user1.id,
            unit="Bier",
            points=-50,
            weekly_allowance=1)
        ex11 = Exercise(
            id=rand_string(30),
            title="Yoga",
            note="Alle Yoga Formen sind OK.",
            user_id=user1.id,
            unit="min",
            points=3)
        # missing: Plank, Wall-Handstand, Superman, Yoga
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

        # Adding UserExercises
        print("appending all user-exercises")
        for user in User.query.all():
            for exercise in Exercise.query.all():
                us_ex = UserExercise(
                    note = exercise.note,
                    exercise_id = exercise.id,
                    user_id = user.id,
                    user = user,
                    points = exercise.points,
                    max_points_day = exercise.max_points_day,
                    max_points_week = exercise.max_points_week,
                    daily_allowance = exercise.daily_allowance,
                    weekly_allowance = exercise.weekly_allowance,
                )
                db.session.add(us_ex)
        db.session.commit()

        print("creating challenge kantnprojekt")
        challenge1 = Challenge(
            id=rand_string(30),
            name="Kantnprojekt",
            description="2000 Punkte pro Kalenderwoche müssen erreicht werden. Diese setzen sich aus allen Übungen inklusive Schlaf und abzüglich Alkohol zusammen.",
            min_points=2000,
            eval_period="week",
            start_date=datetime.datetime.utcnow(),
            end_date=datetime.datetime.utcnow()+datetime.timedelta(days=90))
        db.session.add(challenge1)
        db.session.commit()

        print("appending all challenge exercises...")
        for exercise in Exercise.query.all():
            # print(exercise.title)
            ch_ex = ChallengeExercise(
                note = exercise.note,
                exercise_id = exercise.id,
                challenge_id = challenge1.id,
                challenge = challenge1,
                points = exercise.points,
                max_points_day = exercise.max_points_day,
                max_points_week = exercise.max_points_week,
                daily_allowance = exercise.daily_allowance,
                weekly_allowance = exercise.weekly_allowance,
            )
            db.session.add(ch_ex)
            db.session.commit()
            challenge1.exercises.append(ch_ex)
        db.session.commit()
        print("created all challenge exercises")


        accepted_chall_1 = UserChallenge()
        accepted_chall_1.user = user2
        accepted_chall_1.challenge = challenge1
        print("accepted challenge")
        for ch in user2.challenges:
            print(ch.challenge.name + ":")
            print(" Übungen:")
            for ex in ch.challenge.exercises:
                print("     "+ex.title)
            print(" Teilnehmer:")
            for us in ch.challenge.users:
                print("     "+us.user.user_name)

        print("adding accepted challenge...")
        db.session.add(accepted_chall_1)
        db.session.commit()
        print("adding workouts...")

        wo1 = Workout(
            id=rand_string(30),
            user_id=user2.id,
            date=datetime.datetime(2020, 9, 21, 15, 0, 0,
                                   tzinfo=timezone('CET')),
            note="Test")
        wo2 = Workout(
            id=rand_string(30),
            user_id=user2.id,
            date=datetime.datetime(2020, 9, 20, 15, 0, 0,
                                   tzinfo=timezone('CET')),
            note="Test2")
        db.session.add(wo1)
        db.session.add(wo2)
        db.session.commit()
        print("adding actions...")

        ac1 = Action(
            id=rand_string(30),
            exercise_id=ex6.id, workout_id=wo1.id,
            number=7.5)  # sleep
        ac2 = Action(
            id=rand_string(30),
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
    manager.run()
    # cli()
