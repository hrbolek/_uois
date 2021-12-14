# ReadME

## What is going on

This is a project for students. Students are cooperating on this project under suspicion of teacher.
It is also a model of an information systems which could be used for some administrative task in university life.


## Used technologies

- Python
    - SQLAlchemy for modelling the database entitied
    - FastAPI for API definition and run 
    - Uvicorn as executor of FastAPI
    - Graphene for GaphQL endpoint
    - Tornado for asynchronous HTTP router
    - Pypeteer for data management

- Javascript
    - ReactJS as a library for building bricks of user interface
    - fetch for fetching the data from endpoints

- Docker
    - containerization of applications
    - inner connection of containers
    
- Redis
    - study of usage in IS

- Keycloak
    - autentization server

## Base concept

The project has several docker containers 
- `pyf` Python FastAPI is a container providing an API (GraphQL)
- `js` javascript React is container for UI
- `pyt` Python Tornado is a container which will route HTTP calls from outside of composition of containers
- `nginx` is hardwired router for `pyf\api`, `pyf\gql` and `js\ui`
- `prostgres` is database server
- `pgadmin` is an interface for database server administration

## Who participated on this project
- 2021/9 - 2022/2
    - AS (Teacher)
    - MB (Student, Redis)
    - JB (Student, UI, React)
    - EB (Student, UI, React)
    - VB (Student, Router, Tornado)
    - LH (Student, UI, React)
    - FH (Student, Keycloak, Authentization)
    - JH (Student, Keycloak, Authentization)
    - JJ (Student, UI, React, Python)
    - VM (Student, API, SQLAlchemy, Graphene)
    - JN (Student, Router, Tornado)
    - DP (Student, UI, React)
    - MR (Student, API, SQLAlchemy, Graphene)
    - MS (Student, Redis)
    - DS (Student, Datamanagement, Pypeteer)
    - PV (Student, Datamanagement, Pypeteer)
    - JW (Student, UI, React, Python)

## Current Notes
To run this docker stack in some alpha mode you can run the docker-compose.yml. Be careful as it uses host volumes.