# Face tagging using FB's graph API

A Flask-based front-end to connect to FB's graph API to tag pictures via 
https://github.com/samj1912/fbrecog/.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need docker, docker-compose, docker-machine to spin up the microservices.

### Installing

Spin up the microservices:

```
docker-compose -f .\docker-compose-dev.yml up -d --build
```

Create a database:

```
docker-compose -f docker-compose-dev.yml run imgs-service python manage.py recreate_db
```

Tag faces in the images you put under `services/imgs/project/examples/`
```
docker-compose -f docker-compose-dev.yml run imgs-service python manage.py recognize_ex
```

Browse to `localhost` and query a name through the form.

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Run all the unit tests via:

```
docker-compose -f docker-compose-dev.yml run imgs-service python manage.py test
```

## Built With

* [Flask](http://flask.pocoo.org/)
* [Docker](https://www.docker.com/)
