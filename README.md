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

| Person | Role | Project Job | Period |
|:------:|:----:|:-----------:|:------:|
| AS     |Teacher|                          | 2021/9 - 2022/2 |
| MB     |Student| Redis                    | 2021/9 - 2022/2 |
| JB     |Student| UI, React                | 2021/9 - 2022/2 |
| EB     |Student| UI, React                | 2021/9 - 2022/2 |
| VB     |Student| Router, Tornado          | 2021/9 - 2022/2 |
| LH     |Student| UI, React                | 2021/9 - 2022/2 |
| FH     |Student| Keycloak, Authentization | 2021/9 - 2022/2 |
| JH     |Student| Keycloak, Authentization | 2021/9 - 2022/2 |
| JJ     |Student| UI, React, Python        | 2021/9 - 2022/2 |
| VM     |Student| API, SQLAlchemy, Graphene| 2021/9 - 2022/2 |
| JN     |Student| Router, Tornado          | 2021/9 - 2022/2 |
| DP     |Student| UI, React                | 2021/9 - 2022/2 |
| MR     |Student| API, SQLAlchemy, Graphene| 2021/9 - 2022/2 |
| MS     |Student| Redis                    | 2021/9 - 2022/2 |
| DS     |Student| Datamanagement, Pypeteer | 2021/9 - 2022/2 |
| PV     |Student| Datamanagement, Pypeteer | 2021/9 - 2022/2 |
| JW     |Student| UI, React, Python        | 2021/9 - 2022/2 |


## Current Notes
To run this docker stack in some alpha mode you can run the docker-compose.yml. Be careful as it uses host volumes.