# import os
# basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_ECHO = False
# SQLALCHEMY_TRACK_MODIFICATIONS = True
# # Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
# SQLALCHEMY_DATABASE_URI = "postgres+psycopg2://kantn:password@0.0.0.0:5433/kantnprojekt"
# # have to setup a database



import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgres+psycopg2://kantn:password@0.0.0.0:5433/kantnprojekt")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgres+psycopg2://kantn:password@127.0.0.1:5432/kantnprojekt")
    SQLALCHEMY_TRACK_MODIFICATIONS = False