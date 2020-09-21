#This Dockerfile will spin up nginx server inside our docker container to route the requests from the server to gunicorn which then runs the python scripts
FROM nginx:1.17-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d