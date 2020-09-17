# How to get this thing running

## Pre-Requisits:
- A server which functions as the backend (e.g. Linode or AWS EC2). Ideally, set up remote access via ssh.
- Where git is installed
- install docker: https://docs.docker.com/engine/install/debian/ and docker-compose: https://docs.docker.com/compose/install/. To understand what our docker files are doing, go to https://rollout.io/blog/using-docker-compose-for-python-development/
- nginx installed via `sudo apt-get install nginx`
- python v3.7 or higher. Check with "python --version" that it indeed runs 3.x.x and not 2.7.x
- postgres for database storage, installation via: 
- python packages, installation with requirements.txt

## First time start:
1. Get code via `cd ~ ` and `git clone https://github.com/JoelGotsch/Kantnprojekt_Backend.git`. Alternatively, for easier development you can create ssh keys on the server and add them to your git repo.\
You should now have a new folder with your code in there (in this case the folder name is '`Kantnprojekt_Backend`')\
**optional:** Test the setup:
    - Install a newer python version if version is below 3.8: https://linuxize.com/post/how-to-install-python-3-7-on-debian-9/ (swap 3.7 for newer available version. Or play it safe by using the same one specified in the `Dockerfile`)
    -  for that, install python3 if needed plus `apt-get install python3-venv`\
and create the virtual environment via `python3.8 -m venv venv` which creates the folder venv.
    - Activate the virtual environment via `source venv/bin/activate`
    - Install requirements via `pip install -r requirements.txt`
    - Run `python app.py` which should start a server on `127.0.0.1:8001/`
    - test via `curl 127.0.0.1:8001/api/v0_1/test`
1. Set-up Nginx to connect the public IP adress with localhost:
    - Create an NGINX Configuration file via `sudo nano /etc/nginx/sites-enabled/flaskapp`
    - enter the configuration
  
            server {
                    listen 9123;
                    server_name <Your Linodes IP>;

                    location / {
                            proxy_pass http://127.0.0.1:8001;
                            proxy_set_header Host $host;
                            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    }
            }

    - Unlink the NGINX default config

            unlink /etc/nginx/sites-enabled/default

    -  Reload your NGINX server

            sudo nginx -s reload

1. 
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