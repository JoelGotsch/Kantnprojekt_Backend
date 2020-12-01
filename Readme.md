# How to get this thing running
Great inspiration came from https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/. We will, however, play around with a simpler folder setup and different ports to illustrate what is going on.
Also great is this page: https://morioh.com/p/116ad91ca651 with a little bit more docker commands and the rest remains very similar.

## Pre-Requisits:
- A server which functions as the backend (e.g. Linode or AWS EC2). Ideally, set up remote access via ssh.
- Where git is installed
- install docker: https://docs.docker.com/engine/install/debian/ and docker-compose: https://docs.docker.com/compose/install/. 
- nginx installed via `sudo apt-get install nginx`
- python v3.7 or higher. Check with "python --version" that it indeed runs 3.x.x and not 2.7.x
- postgres for database storage, installation via: 
- python packages, installation with requirements.txt

## First time start:
1. Install and set up PostgreSQL. We need to create a user "kantn" and a database "kantnprojekt" with password "password" on port `127.0.0.1` and port `5433`(which we will also use within the docker environment, so things don`t change). Also see https://wiki.debian.org/PostgreSql
    - `apt-get update` and `apt-get install postgresql` `createuser kant
    - create role `kantn` (= database username): `sudo -i -u postgres` (now you switched to the postgres user)
    - create the database `createdb kantnprojekt`
    - set password for user: `psql` and then `alter user kantn with encrypted password 'password';` (console should print `ALTER ROLE`)
    - give permission to user: `psql` and then `grant all privileges on database kantnprojekt to kantn;` (console should print `GRANT`)
    - Quit the postgres terminal via `\q` and hit return.
Useful commands:
        - `service postgresql status\start\stop`
1. Get code via `cd ~ ` and `git clone https://github.com/JoelGotsch/Kantnprojekt_Backend.git`. Alternatively, for easier development you can create ssh keys on the server and add them to your git repo.\
You should now have a new folder with your code in there (in this case the folder name is '`Kantnprojekt_Backend`')\
**optional:** Test the setup:
    - Install a newer python version if version is below 3.8: https://linuxize.com/post/how-to-install-python-3-7-on-debian-9/ (swap 3.7 for newer available version. Or play it safe by using the same one specified in the `Dockerfile`)
    -  for that, install python3 if needed plus `apt-get install python3-venv`\
and create the virtual environment via `python3.8 -m venv venv` which creates the folder venv.
    - Activate the virtual environment via `source venv/bin/activate`
    - Install requirements via `pip install -r services/web/requirements.txt` (it is in there, because the docker container needs it too later)
    <!-- - Run `python app.py` which should start a server on `127.0.0.1:8001/`
    - test via `curl 127.0.0.1:8001/api/v0_1/test`, this should yield a `"status": "success"` message. -->
1. Set-up VS Code properly so that Pylance will detect the imports. This is necessary as the folder structure in the docker container will be different and the imports need to work for that.
    - Go to settings via "Strg+Shift+P", enter settings (UI), go to Extensions, chose Pylance and for extra-path argument use "/home/Kantnprojekt_Backend/services/web".
1. Set-up Nginx to connect the public IP adress with localhost:
    - Create an NGINX Configuration file via `sudo nano /etc/nginx/sites-enabled/kantnprojekt`
    - enter the configuration (port 80 is used as it is the standard web port and we can therefore just put in the url later without naming a port). We use port 8002 because the gunicorn WSGI will use that port.
  
          server {
                listen 80;
                server_name <Your Linodes IP>;

                location / {
                        proxy_pass http://127.0.0.1:8003;
                        proxy_set_header Host $host;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                }
          }

    - Unlink the NGINX default config

            unlink /etc/nginx/sites-enabled/default

    -  Reload your NGINX server

            sudo nginx -s reload
    
        **optional**: Test this from your computer via browser:
        - Start with  `python wsgi.py` which should start a server on `127.0.0.1:8002/`
        - "http://\<LinodeIP\>:80/api/v0_1/test" or "http://\<LinodeIP\>/api/v0_1/test"
1. Initial setup of our database:
    - `cd /home/Kantnprojekt_Backend/`; activate virtual environment `source venv/bin/activate`; `cd services/web/`
    - `python manage.py create_db` deletes old db and creates new empty one.
    - `python manage.py seed_db` puts in some exercises, users and workouts to have a minimal working example to play around with.
    - `python manage.py db init` this makes future migrations of the database possible. Flask-migrate is used for that and it will create a folder `versions` which hold the relevant information for this database upgrades and downgrades. This should be checked into your git-repository. For more information what you can do with flask-migration visit https://flask-migrate.readthedocs.io/en/latest/
    - *Optional*: View contents of table: `psql --host=localhost --dbname=kantnprojekt --username=kantn`. You will be asked for the password, which we set to 'password'. Then `\dt+` to see a list of the tables. SQL commands work too: `SELECT * FROM exercises;` (exit via `q`)

1. Next step: using gunicorn: `gunicorn -w 3 kantn` (making 3 worker processes)

1. Now shifting everything inside a docker container and using gunicorn. To understand what our docker files are doing, go to https://rollout.io/blog/using-docker-compose-for-python-development/:
   - As we will use the 8002 port only within the docker container and nginx running inside the container is looking for the 8003 port to map it to the 8002 port, we have to switch the nginx configuration on the server:
   `sudo nano services/nginx/nginx.conf`

            upstream kantnprojekt_backend{
                server web:8002;
            }

            server {

                listen 8001;

                location / {
                    # kantnprojekt_backend  as defined above!!
                    # OLD: kantnprojekt_backend or kantnprojekt_backend_default should be the default network address created by the docker-compose action https$
                    proxy_pass http://kantnprojekt_backend;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header Host $host;
                    proxy_redirect off;
                }

            }


   - Run again `sudo nano /etc/nginx/sites-enabled/kantnprojekt` and change the "8002" to "8003". Save and exit. Restart the nginx server with `sudo nginx -s reload`. \
   NOTE: If these ports should be changed, look into the docker-compose file as well as the services/nginx/nginx.config file.
   - Run: (-d: dispatch, runs in background, --build: makes sure the container is built again)

         docker-compose -f docker-compose.prod.yml down -v
         docker-compose -f docker-compose.prod.yml up -d --build
         docker-compose -f docker-compose.prod.yml exec web python manage.py create_db

2. 
- migrate.py commands to create postgres database
- start app via ...
- test api via ...

## Useful docker commands
- To step into a docker container bash run `docker container ls` to see the docker containers and their names which are running. In this case we want to have a shell in `kantnprojekt_backend_web_1`. We also want to be root, so we set the user to that, otherwise we would be "app" which can't install anything. So the command is `docker exec --user "root" -it kantnprojekt_backend_web_1 /bin/bash`.
- 

## How to change/ adapt code:

### Data-Model Changes:
This is based on https://flask-migrate.readthedocs.io/en/latest/.
- change in models.py
- if docker container is running, bash into the container (see Useful docker commands), `cd project` and `python migrate.py db migrate`. This creates a migration file.

### API new endpoint creation/changes:
For changes: If the API return is in a different format (new variables), then the version should change and a git-branch should be created. Otherwise, the new code can just be pushed to the current branch and run.
- create new branch in git
- adapting the "__version__" variable in app.py
- create file in resources (see other files as templates)
- add route in app.py
- run new backend.