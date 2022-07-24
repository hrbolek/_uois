# ReadME

## What is going on

This is a project for students. Students are cooperating on this project under suspicion of teacher.
It is also a model of an information systems which could be used for some administrative task in university life.


## Used technologies

- Python
    - SQLAlchemy for modelling the database entitied (async queries)
    - FastAPI for API definition and run 
    - Uvicorn as executor of FastAPI
    - Strawberry for GraphQL endpoint (federated GraphQL)
    - Appolo federation for GraphQL federation queries

- Javascript
    - ReactJS as a library for building bricks of user interface
    - fetch for fetching the data from endpoints

- Docker
    - containerization of applications
    - inner connection of containers
    
- Postgres 
    - and its compatible replacements

## Base concept

The project has several docker containers 
- `apollo` master of federation
- `gql_*` apollo federation member
- `nginx` is hardwired router 
- `prostgres` is database server
- `pgadmin` is an interface for database server administration

## Who participated on this project

| Person | Role | Project Job | Period |
|:------:|:----:|:-----------:|:------:|
| AS     |Teacher|                          | 2022/9 - 2023/2 |


## Current Notes
To run this docker stack in some alpha mode you can run the docker-compose.yml. Be careful as it uses host volumes.