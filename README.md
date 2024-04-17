# flowkadjango
Flowka with Django

## Managing files

# Data

# Pictures


## Cleaning Data


## Architecture

### Django + Unicorn

### Media and Static on Docker + Nginx


**staging**
Flowka75lt03
*docker setup*
    docker run --name fl-nginx -p 8000:80 -d -v /home/flowka:/usr/share/nginx/html nginx

### SFTP storage

**dev**
flowka75lt02

**staging**
Flowka75lt03


### Minio + Docker


*Swarm Manager*
Flowka75lt07

*Swarm workers*
Flowka75lt08

### RabbitMQ + docker

*manager*
Flowka75lt03

*nodes*
Flowka75lt07
Flowka75lt08


### Caching


### Load balancing
