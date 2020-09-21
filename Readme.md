# How to get this thing running
Great inspiration came from https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/. We will, however, play around with a simpler folder setup and different ports to illustrate what is going on.

## Pre-Requisits:
- A server which functions as the backend (e.g. Linode or AWS EC2). Ideally, set up remote access via ssh.
- Where git is installed
- install docker: https://docs.docker.com/engine/install/debian/ and docker-compose: https://docs.docker.com/compose/install/. 
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
    - test via `curl 127.0.0.1:8001/api/v0_1/test`, this should yield a `"status": "success"` message.
1. Set-up Nginx to connect the public IP adress with localhost:
    - Create an NGINX Configuration file via `sudo nano /etc/nginx/sites-enabled/kantnprojekt`
    - enter the configuration (port 80 is used as it is the standard web port and we can therefore just put in the url later without naming a port). We use port 8002 because the gunicorn WSGI will use that port.
  
          server {
                listen 80;
                server_name <Your Linodes IP>;

                location / {
                        proxy_pass http://127.0.0.1:8002;
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
1. Next step: using gunicorn: `gunicorn -w 3 kantn

1. Now shifting everything inside a docker container and using gunicorn. To understand what our docker files are doing, go to https://rollout.io/blog/using-docker-compose-for-python-development/:
   - As we will use the 8002 port only within the docker container and nginx running inside the container is looking for the 8003 port to map it to the 8002 port, we have to switch the nginx configuration on the server:
   - Run again `sudo nano /etc/nginx/sites-enabled/kantnprojekt` and change the "8002" to "8003". Save and exit. Restart the nginx server with `sudo nginx -s reload`. \
   NOTE: If these ports should be changed, look into the docker-compose file as well as the services/nginx/nginx.config file.
   - Run:

         docker-compose -f docker-compose.prod.yml down -v
         docker-compose -f docker-compose.prod.yml up -d --build
         docker-compose -f docker-compose.prod.yml exec web python manage.py create_db

2. 
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