SHELL := /bin/bash
##  gunicorn and hot-reload
## from: https://blog.theodo.com/2020/05/debug-flask-vscode/

gunicorn:
	# if containers are already running, shut them down so that api calls get to the newly created containers where we debug, not the old ones we don't observe. duh.
	docker-compose -f docker-compose.debug.yml down -v
	docker-compose -f docker-compose.prod.yml down -v
	# creating and starting the containers
	docker-compose -f docker-compose.prod.yml up -d --build


reset:
	# if containers are already running, shut them down so that api calls get to the newly created containers where we debug, not the old ones we don't observe. duh.
	docker-compose -f docker-compose.debug.yml down -v
	docker-compose -f docker-compose.prod.yml down -v
	docker-compose -f docker-compose.debug.yml up -d --build
	docker-compose -f docker-compose.debug.yml exec web python manage.py create_db
	docker-compose -f docker-compose.debug.yml exec web python manage.py seed_db
	docker-compose -f docker-compose.debug.yml exec web python manage.py db init
	docker-compose -f docker-compose.debug.yml exec web python manage.py db upgrade


gunicorndebug:
	# if containers are already running, shut them down so that api calls get to the newly created containers where we debug, not the old ones we don't observe. duh.
	# docker-compose -f docker-compose.debug.yml down -v
	# docker-compose -f docker-compose.prod.yml down -v
	# creating and starting the containers
	docker-compose -f docker-compose.debug.yml up -d --build
	# docker-compose -f docker-compose.debug.yml exec web python manage.py create_db
	# docker-compose -f docker-compose.debug.yml exec web python manage.py create_db
	# docker-compose -f docker-compose.debug.yml exec web python manage.py seed_db

	# now we can look at the logs via "docker logs -t kantnprojekt_backend_web_1". It should say "VS Code debugger can now be attached, press F5 in VS Code.."
	# do that: we configured a python attach configuration for debugging in .vscode/launch.json which searchs for the open port and thus connecting the debugger to the docker

debug_backup:
	# if containers are already running, shut them down so that api calls get to the newly created containers where we debug, not the old ones we don't observe. duh.
	docker-compose -f docker-compose.debug.yml down -v
	# docker-compose -f docker-compose.prod.yml down -v
	# creating and starting the containers
	# docker-compose -f docker-compose.debug.yml run --rm --service-ports web gunicorn --reload --bind 0.0.0.0:8002 --timeout 3600 manage:app
	docker-compose -f docker-compose.debug.yml up -d --build
	docker-compose -f docker-compose.debug.yml exec web python manage.py create_db
	docker-compose -f docker-compose.debug.yml exec web python manage.py restore_backup_dump_docker

debug_reuse:
	# if containers are already running, shut them down so that api calls get to the newly created containers where we debug, not the old ones we don't observe. duh.
	docker-compose -f docker-compose.debug.yml down -v
	docker-compose -f docker-compose.prod.yml down -v
	# creating and starting the containers
	# docker-compose -f docker-compose.debug.yml run --rm --service-ports web gunicorn --reload --bind 0.0.0.0:8002 --timeout 3600 manage:app
	# docker-compose -f docker-compose.debug.yml exec web python manage.py create_db
	docker-compose -f docker-compose.debug.yml up -d

debug_upgrade_database:
	# if containers are already running, shut them down so that api calls get to the newly created containers where we debug, not the old ones we don't observe. duh.
	docker-compose -f docker-compose.debug.yml down -v
	docker-compose -f docker-compose.prod.yml down -v
	docker-compose -f docker-compose.debug.yml up -d --build
	docker-compose -f docker-compose.debug.yml exec web python project/migrate.py db migrate
	# now bash into container with docker exec --user "root" -it kantnprojekt_backend_web_1 /bin/bash, adapt the migration file and then run
	# docker-compose -f docker-compose.debug.yml exec web python project/migrate.py db upgrade
