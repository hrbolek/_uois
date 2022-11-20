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
| AS     |Teacher| gql_ug                   | 2022/9 - 2023/2 |
| AS     |Teacher| gql_workflows            | 2022/9 - 2023/2 |
| AS     |Teacher| gql_externalids          | 2022/9 - 2023/2 |

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
