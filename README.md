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
- `frontend` provides static files = REACT compiled items (including GQL interface)
- `gql_*` apollo federation member
- `nginx` is hardwired router
- `prostgres` is database server
- `pgadmin` is an interface for database server administration

## Who participated on this project

| Person | Role  | Project Job              | Period          |
|:------:|:-----:|:------------------------:|:---------------:|
| AS     |Teacher|                          | 2022/9 - 2023/2 |
| AS     |Teacher| gql_ug                   | 2022/9 - 2023/2 |
| AS     |Teacher| gql_workflows            | 2022/9 - 2023/2 |
| AS     |Teacher| gql_externalids          | 2022/9 - 2023/2 |
| S+V    |Student| gql_facilities           | 2022/9 - 2023/2 |
| B+Z    |Student| gql_events               | 2022/9 - 2023/2 |
| R+M    |Student| gql_attendance           | 2022/9 - 2023/2 |
| D+V    |Student| gql_granting             | 2022/9 - 2023/2 |
| K+C    |Student| gql_thesis               | 2022/9 - 2023/2 |
| N+N    |Student| gql_lessons              | 2022/9 - 2023/2 |
| D+N    |Student| gql_forms                | 2022/9 - 2023/2 |
| P+B    |Student| gql_publications         | 2022/9 - 2023/2 |
| H+L    |Student| gql_personalities        | 2022/9 - 2023/2 |
| Ch+H   |Student| gql_projects             | 2022/9 - 2023/2 |
| R+S    |Student| gql_surveys              | 2022/9 - 2023/2 |
|        |       |                          |                 |
| AS     |Teacher|                          | 2023/3 - 2023/6 |
| AS     |Teacher| frontend                 | 2023/3 - 2023/6 |
| AS     |Teacher| gql_preferences          | 2023/3 - 2023/6 |
|        |       | frontend - lessons       | 2023/3 - 2023/6 |
|        |       | frontend - users+groups  | 2023/3 - 2023/6 |
|        |       | frontend - facilities    | 2023/3 - 2023/6 |
|        |       | frontend - projects      | 2023/3 - 2023/6 |
|        |       | frontend - publications  | 2023/3 - 2023/6 |
|        |       | frontend - presences     | 2023/3 - 2023/6 |
|        |       | frontend - events        | 2023/3 - 2023/6 |
|        |       | frontend - surveys       | 2023/3 - 2023/6 |
|        |       | frontend - workflow      | 2023/3 - 2023/6 |
|        |       | frontend - authorizations| 2023/3 - 2023/6 |

## Current Notes
To run this docker stack in some alpha mode you can run the docker-compose.yml. Be careful as it uses host volumes.

There is problem with sessions and persistence of SQLAlchemy memory objects which has been solved with introduction of derived class.
This class open a session, store it and allow to access it trought context

A healthcheck has been added to docker-compose. It is based on QGL endpoint. The query retrieves list of entities.
Unfortunatelly unhealthy containers are not restarted.

The federation uses resolve_reference class method to instantiate a class.
This must be solved in federation member which is responsible for the type (class) but also in federation member which extends this type
Both methods are implemented by different way.

All federation members has asynchronous inicialization which is done during first question to a federation member.
This first question is send by apollo container which asks all federation members to provide a particular schema.
Apollo then create a "super" schema and starts to serve queries.
Apollo must be started after all federation members are alive and ready to serve.

During initialization is possible to store type lists (as is used) which acts as a system data.

gql_ug provides data structures for users, groups, their relations and types.
There are also roles which allow to define a member which plays a special role in a group.

gql_externalids is probably the simplest federation member.
It allows to link external ids, from other information systems to internal ids.
A user can have several ids. In IS this can be used for visualisation of link to other IS.
This federation member extends users and groups.

gql_workflow manages a statefull machine on processed data structures.

gql_empty is template for a federation member.
It allows to quite fast implement a new federation member.
It is expected that this order is followed:

1. DBDefinitions.py contains a db models (based on SQLAlchemy).

2. GraphResolvers.py contains a functions for mapping a set of parameters into a DB based result.
There is a library (out of Pypi) which has a set of functions creating a standard resolvers.

3. GraphTypeDefinitions.py contains a GraphQL models (based on Strawberry).
Resolvers should be taken from step 2.

4. DBFeeder.py contains a scripts for DB initializations

5. Do not forget to extend docker-compose.yml. Simply copy existing gql service and change context (and ports).
Also server.js in apollo container must be extended.

## Lessons learned
## Naming convention
Names should be composed according given naming convention.
DB table names should be in plural.
Foreign keys should be in singular followed by undescore and id (aka user_id).
Both table name and attribute name should not have capitalized letters otherwise there may be conficts in some db servers.
SQLAlchemy models should be in singular followed by Model (aka UserModel).
GraphQL models should be in singulart form folowed by GQLModel (aka UserGQLModel).

### Hybrid development
There are groups of tasks which can be developen and run isolated.
The first is development of db structure and sqlalchemy models.
The second is development of resolvers and retrieving data from database
The third is development of qraphQL models outside of federation.

All those steps can be done in Jupyter which can help in most cases. To prepare this a user should be familiar with commands:

`docker run -d --restart unless-stopped --name jupyterdevelop -p 8888:8888 -p 8999:9992 -v "C:\FULLPATH\TO\dirwithipnb\files":/home/jovyan/work jupyter/scipy-notebook`

The new container will be named "jupyterdevelop".

As the container will be out of docker stack, it must be connected to other containers (especially with postgres). To configure this, use the next command
see (https://docs.docker.com/engine/reference/commandline/network_connect/)

`docker network connect --alias jupyter uois_default jupyterdevelop`

The container will be joined with network "uois_default" which is default network name for this project. Also the container will be available inside this network with host name "jupyter". Such connection allows to use same connection strings in jupyter environment as in the project.

### DB
In asynchronous environment it should be used context managers creating sessions. If single session is created for call errors could occur.
This is not deterministic behaviour. The problem appears more often if query trought multiple federation members is asked.

As this project aim for distributed usage (API and  web UI), some concurency editing could happen. This must be detected.
Timestamp as an attribute can play this role. For this project has been chosen

`lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())`

Use of UUID as primary key can help in many cases, especially when importing data. Unfortunately this is not supported by many DB systems.

At some stage you can find usefull to drop all tables. It is possible to use next commands.

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;


### Strawberry / GraphQL
Strawberry has not support for multiple references resolution. This could slow down the response construction significantly.
Dataloaders do not solve this problem. They can help only in some cases. Federation schema must be updated especially method resolve reference.

Top on this, creation of Dataloaders working with Redis would make a miracle regarding the server response time.

## Monitoring
There are some libraries, included in Strawberry. Also Prometheus would be taken into account.


## Proper initialization
If the database is not initialized with SQL script, the containers should be run in this order:
1. gql_ug
2. gql_externalids
3. gql_workflow
4. gql_events
5. gql_facilities
6. gql_personalities
7. gql_surveys
8. gql_publications
9. gql_forms
10. gql_presences
11. gql_lessons
12. gql_projects

some containers in the list can be run simultaneously

latest versions introduced DB decoupling so all containers could run separate DB engines

## UI Catalog
Storybook in frontend is used

## Monorepo
Frontend is structured as nodejs monorepo. There are several libraries and two applications.

- frontend UI itself
- Storybook as component catalog

both of them are located in apps directory
All libraries are in directory packages.

## Multistage dockefile
Frontend has multistage dockerfile with stages related to python server (serving frontend files) 
and stages for build particular js applications.