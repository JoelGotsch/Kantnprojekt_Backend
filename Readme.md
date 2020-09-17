# How to get this thing running

## Pre-Requisits:
- A server which functions as the backend (e.g. Linode or AWS EC2). Ideally, set up remote access via ssh.
- git installed
- install docker: https://docs.docker.com/engine/install/debian/ and docker-compose: https://docs.docker.com/compose/install/. To understand what our docker files are doing, go to https://rollout.io/blog/using-docker-compose-for-python-development/
- python v3.7 or higher. Check with "python --version" that it indeed runs 3.x.x and not 2.7.x
- postgres for database storage, installation via: 
- python packages, installation with requirements.txt

## First time start:
- create virtual env via "python -m venv venv"
- migrate.py commands to create postgres database
- start app via ...
- test api via ...

## How to change/ adapt code:

### Data-Model Changes:
- change in models.py
- run "python migrate.py update/upgrade"

### API new endpoint creation/changes:
For changes: If the API return is in a different format (new variables), then the version should change and a git-branch should be created. Otherwise, the new code can just be pushed to the current branch and run.
- create new branch in git
- adapting the "__version__" variable in app.py
- create file in resources (see other files as templates)
- add route in app.py
- run new backend.