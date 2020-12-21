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

deploymentv2Api:
	# in nginx rerouting to v0_2 needs to be done!
	docker-compose -f docker-compose.debug.yml exec postgres pg_dump -U kantn -d kantnprojekt_db > /home/Kantnprojekt_Backend/services/web/project/backups/backup.dump
	docker-compose -f docker-compose.debug.yml down -v
	docker-compose -f docker-compose.prod.yml down -v
	docker-compose -f docker-compose.debug.yml up -d --build
	# the backup-file neeeds some ordering to work properly!
	docker-compose -f docker-compose.debug.yml exec -T postgres psql -U kantn -d kantnprojekt_db < /home/Kantnprojekt_Backend/services/web/project/backups/2020-12.21.dump
	docker-compose -f docker-compose.debug.yml exec -T postgres psql -U kantn -d kantnprojekt_db < /home/Kantnprojekt_Backend/services/web/project/backups/2020-12.21.dump
	docker-compose -f docker-compose.debug.yml exec -T postgres psql -U kantn -d kantnprojekt_db < /home/Kantnprojekt_Backend/services/web/project/backups/2020-12.21.dump
	docker-compose -f docker-compose.debug.yml exec -T postgres psql -U kantn -d kantnprojekt_db < /home/Kantnprojekt_Backend/services/web/project/backups/2020-12.21.dump
	docker-compose -f docker-compose.debug.yml exec -T postgres psql -U kantn -d kantnprojekt_db < /home/Kantnprojekt_Backend/services/web/project/backups/2020-12.21.dump
	docker-compose -f docker-compose.debug.yml exec -T postgres psql -U kantn -d kantnprojekt_db < /home/Kantnprojekt_Backend/services/web/project/backups/2020-12.21.dump
	# docker-compose -f docker-compose.debug.yml exec web python manage.py db migrate
	# docker-compose -f docker-compose.debug.yml exec web python manage.py db upgrade
	docker-compose -f docker-compose.debug.yml exec web python manage.py add_missing_user_exercises
	docker-compose -f docker-compose.debug.yml exec web python manage.py start_kantnprojekt_december

# situation: you used flask and changed some data in the database, now you want it running in docker
docker_from_local:
	# if containers are already running, shut them down so that api calls get to the newly created containers where we debug, not the old ones we don't observe. duh.
	# docker-compose -f docker-compose.debug.yml exec postgres pg_dump -U kantn -d kantnprojekt_db > /home/Kantnprojekt_Backend/services/web/project/backups/backup.dump
	# create backup from local postgres database:
	venv/bin/python3 services/web/manage.py backup_dump --filename local_backup.dump
	docker-compose -f docker-compose.debug.yml down -v
	# creating and starting the containers
	docker-compose -f docker-compose.debug.yml up -d --build
	docker-compose -f docker-compose.debug.yml exec web python manage.py create_db
	#old way: use python within the web - docker (needs to install postgres there). better: use the file from outside directly
	# docker-compose -f docker-compose.debug.yml exec web python manage.py restore_backup_dump_docker
	# for some reason we need the -T flag here: https://github.com/docker/compose/issues/7306
	# other than that, it executes the psql command (which reads in a sql script) within the postgres service
	# multiple times is needed, as for some reason there is an issue with foreign keys in the dump. So it only adds those tables where its allowed to add something based on the data which is already there.
	docker-compose -f docker-compose.debug.yml exec -T postgres psql -U kantn -d kantnprojekt_db < /home/Kantnprojekt_Backend/services/web/project/backups/local_backup.dump
	docker-compose -f docker-compose.debug.yml exec -T postgres psql -U kantn -d kantnprojekt_db < /home/Kantnprojekt_Backend/services/web/project/backups/local_backup.dump
	docker-compose -f docker-compose.debug.yml exec -T postgres psql -U kantn -d kantnprojekt_db < /home/Kantnprojekt_Backend/services/web/project/backups/local_backup.dump
	docker-compose -f docker-compose.debug.yml exec -T postgres psql -U kantn -d kantnprojekt_db < /home/Kantnprojekt_Backend/services/web/project/backups/local_backup.dump
	docker-compose -f docker-compose.debug.yml exec -T postgres psql -U kantn -d kantnprojekt_db < /home/Kantnprojekt_Backend/services/web/project/backups/local_backup.dump

create_backup_docker:
	docker-compose -f docker-compose.debug.yml exec postgres pg_dump -U kantn -d kantnprojekt_db > /home/Kantnprojekt_Backend/services/web/project/backups/backup.dump
	

debug_reuse:
	# if containers are already running, shut them down so that api calls get to the newly created containers where we debug, not the old ones we don't observe. duh.
	docker-compose -f docker-compose.debug.yml down -v
	docker-compose -f docker-compose.prod.yml down -v
	# creating and starting the containers
	# docker-compose -f docker-compose.debug.yml run --rm --service-ports web gunicorn --reload --bind 0.0.0.0:8002 --timeout 3600 manage:app
	# docker-compose -f docker-compose.debug.yml exec web python manage.py create_db
	docker-compose -f docker-compose.debug.yml up -d

# debug_upgrade_database:
# 	# if containers are already running, shut them down so that api calls get to the newly created containers where we debug, not the old ones we don't observe. duh.
# 	docker-compose -f docker-compose.debug.yml down -v
# 	docker-compose -f docker-compose.prod.yml down -v
# 	docker-compose -f docker-compose.debug.yml up -d --build
# 	docker-compose -f docker-compose.debug.yml exec web python project/migrate.py db migrate
# 	# now bash into container with docker exec --user "root" -it kantnprojekt_backend_web_1 /bin/bash, adapt the migration file and then run
# 	# docker-compose -f docker-compose.debug.yml exec web python project/migrate.py db upgrade

extract_docker_data_to_local:
	# first make backup of current local database so we don't mess anything up:
	# venv/bin/python3 services/web/manage.py backup_dump
	# export PGPASSWORD='password'; pg_dump -U kantn --host=localhost -d kantnprojekt > /home/Kantnprojekt_Backend/services/web/project/backups/backup.dump
	# now make the backup from docker-container:
	docker-compose -f docker-compose.debug.yml exec postgres pg_dump -U kantn -d kantnprojekt_db > /home/Kantnprojekt_Backend/services/web/project/backups/backup.dump
	# now load the backup
	export PGPASSWORD='password'; psql -U kantn --host=localhost -d kantnprojekt2 < /home/Kantnprojekt_Backend/services/web/project/backups/backup.dump
	export PGPASSWORD='password'; psql -U kantn --host=localhost -d kantnprojekt2 < /home/Kantnprojekt_Backend/services/web/project/backups/backup.dump
	export PGPASSWORD='password'; psql -U kantn --host=localhost -d kantnprojekt2 < /home/Kantnprojekt_Backend/services/web/project/backups/backup.dump
	export PGPASSWORD='password'; psql -U kantn --host=localhost -d kantnprojekt2 < /home/Kantnprojekt_Backend/services/web/project/backups/backup.dump
	export PGPASSWORD='password'; psql -U kantn --host=localhost -d kantnprojekt2 < /home/Kantnprojekt_Backend/services/web/project/backups/backup.dump
	# venv/bin/python3 services/web/manage.py restore_backup_dump --filename backup.dump
	# now you can run Python:Flask debug settings in VS Code and start debugging
