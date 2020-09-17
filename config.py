import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
SQLALCHEMY_DATABASE_URI = "postgres+psycopg2://app:<PW>@localhost:5432/kantnprojekt"
# have to setup a database