# everything handled now in manage.py
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import pathlib
parent_path_long = pathlib.Path(__file__).absolute()
parent_path = parent_path_long.parents[1].absolute()
print(parent_path)
import sys
# made to work inside docker container:
sys.path.append(parent_path)
from project import app, db

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()