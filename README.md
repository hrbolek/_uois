# ReadME

## What is going on

This is a project for students. Students are cooperating on this project under supervision of teacher.
It is also a model of an information systems which could be used for some administrative task in university life.

## Used technologies

- Python (see https://www.python.org/)
    - SQLAlchemy for modelling the database entitied (async queries) (see https://www.sqlalchemy.org/)
    - FastAPI for API definition and run (see https://fastapi.tiangolo.com/)
    - Uvicorn as executor of FastAPI (see https://www.uvicorn.org/)
    - Strawberry for GraphQL endpoint (federated GraphQL) (see https://strawberry.rocks/)
    - Appolo federation for GraphQL federation queries (see https://www.apollographql.com/docs/federation/)

- Javascript (see https://developer.mozilla.org/en-US/docs/Web/JavaScript)
    - ReactJS as a library for building bricks of user interface (see https://react.dev/)
    - fetch for fetching the data from endpoints

- Docker (see https://www.docker.com/)
    - containerization of applications
    - inner connection of containers
    - deployment of service stacks (see https://docs.docker.com/compose/)

- Postgres (see https://www.postgresql.org/)
    - and its compatible replacements (Yugabyte - https://www.yugabyte.com/, Cockroach - https://www.cockroachlabs.com/)
    - can be also used, with small refactoring (thanks to SQLalchemy), different SQL engine such MSSQL, MariaDB, etc.

## Base concept

The project has several docker containers
- `apollo` master of federation
- `frontend` provides static files = REACT compiled items (including GQL interface)
- `gql_*` apollo federation member
- `prostgres` is database server
- `pgadmin` is an interface for database server administration (see https://www.pgadmin.org/)

## Security

There should be a authority which create jwt (json web token see https://jwt.io/introduction) by standard rfc7519 (see https://datatracker.ietf.org/doc/html/rfc7519).
Authority must expose http endpoint providing (via GET verb) public key (signing algorithm RS256, see https://crypto.stackexchange.com/questions/104184/is-this-how-rs256-works-in-jwt) and also http endpoint (via GET verb with token) user info based on included token.
User is authenticated if its cookie authorization has valid jwt. This jwt is validated to authority.

Because whole deployment has several parts, each part receives a http request with token and this token is always validated.


    --> Frontend --> Authority (key)
        Frontend <-- Authority (key)
        Frontend ----------------------> Federation
                                         Federation --> MemberA --> Authority (key)
                                         Federation --> MemberB --> Authority (key)
                                                        MemberA <-- Authority (key)
                                                        MemberB <-- Authority (key)
                                         Federation <-- MemberA
                                         Federation <-- MemberB
        Frontend <---------------------- Federation

The public key is cached. 
If the incomming jwt is not valid, public key is refreshed. 
If jwt is not valid even with new public key, the http request is handled as unathenticated.
For frontend server (html pages) the appropriate response is redirect (to login).
For GQL server (apollo federation) response holds a code.

Authority is integrated in frontend. The design allows to refactor it for Keycloack (see https://www.keycloak.org/) as an example.

## Frontend applications

As there is strong API (GQL based), frontend can decoupled into simple SPA (Single page application see https://developer.mozilla.org/en-US/docs/Glossary/SPA) htmls.
The frontend server manages catalog of such pages (see `/server/htmls` and `/server/config.json`). 
According this catalog the landing page is generated.
Entry points are guarded for unathenticated users.
Such attemps are redirected to login page.

It is expected that frontend applications are developed with ReactJS library (see https://react.dev/).
To share forged application segments - components there should be catalog of components (see https://storybook.js.org/).
If the application is a bit more complex there are accomodated conceps of central storage (see https://react-redux.js.org/) working with state functions and immutable state (see https://immerjs.github.io/immer/ and https://redux-toolkit.js.org/).

### Special applications

The deployment structure allows to accomodate applications from foreign sources.
Currently there are two of them.
- GraphiQL, which allows to send queries in raw mode (see https://www.gatsbyjs.com/docs/how-to/querying-data/running-queries-with-graphiql/)
- Voyager, which displays the ERD (Entity relation diagram) for GraphQL endpoint (see https://graphql-kit.com/graphql-voyager/)

## Backend containers

As has been introduced earlier, there are several containerized applications which are GraphQL federation members.
Each of them should provide set of entities and sometimes extend external entities behaviour.
To provide entities itself, there is somep point at which the row in database table is retrieved and server.
To fulfill this, row must be identified. For such identification uuid is used - primary key is uuid (see https://en.wikipedia.org/wiki/Universally_unique_identifier).
Such approach allows to generate primary keys in distributed way which helps in several ways (even in testing phase).
For reading from database the SQLAlchemy library is used. Also to improve concurency, there are asynchronous dataloaders (see https://github.com/syrusakbary/aiodataloader).
This concept solves the N+1 problem (see https://planetscale.com/blog/what-is-n-1-query-problem-and-how-to-solve-it).
It also allows to use Redis (see https://redis.io/) to improve data throughtput.

To decide which entities and its attributes are allowed to operate on, the strawberry introduced permission classes (see https://strawberry.rocks/docs/guides/permissions).
This is high granularity tool which perfectly fits the needs. 
It is commond that entities have their rbacobject (uuid key) from which is possible to derive who can work with entity or/and its attributes. 

rbacobject can be an user id or group id.
In both casese there are users in roles for the group (rbacobject) and its mastergoups or in groups and its mastergroups where an user (rbacobject) is member.
For a point (entity or/and its attributes) there can be enlisted needed roles (reading and writing rights for queries and mutations).
Only if logged user (identified by the token), has appropriate roles towards rbacobject, then operation is allowed.

## Deployment

As minimal configuration there are
  - frontend (authority, html page provider, proxy to api)
  - apollo (covers all federation members thus it is also indirectly proxies them)
  - gql_ug provides roles so must be in every deployment
  - gql_forms (standard federation member)

Database is deployed outside of this stack (see `host.docker.internal:5432`)

```yaml
version: "3.9"

services:
  apollo:
    image: hrbolek/apollo_federation
    # image: apollofederation:latest
    environment:
      # promenne, ktere lze cist v kontejneru
      - PORT=3000
      - |
        SERVICES=
        [
          {"name": "ug", "url": "http://gql_ug:8000/gql"},
          {"name": "forms", "url": "http://gql_forms:8000/gql"}
        ]
    healthcheck:
      # definice, umoznujici provest test, zda je kontejner v poradku (vsimnete si portu a srovnejte s portem v environment)
      interval: 60s
      retries: 3
      start_period: 60s
      timeout: 10s
    restart: on-failure:3 # nedojde k restartu pokud je kontejner "unhealthy", maximalne 3 pokusy
    # ports: #v deploymentu by nebylo zadne mapovani portu
      # vnejsi port : port, kde sluzbu poskytuje kontejner
      # - 33000:3000
    depends_on:
      - gql_ug
      - gql_forms

  gql_ug:
    image: hrbolek/gql_ug
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=example
      - POSTGRES_HOST=host.docker.internal:5432
      - POSTGRES_DB=data
      - JWTPUBLICKEYURL=http://frontend:8000/oauth/publickey
      - JWTRESOLVEUSERPATHURL=http://frontend:8000/oauth/userinfo
      - DEMO=True
    healthcheck:
      # definice, umoznujici provest test, zda je kontejner v poradku
      test: "curl -f -H 'Content-Type: application/json' -X POST -d '{\"query\":\"query{__schema{types{name}}}\"}' http://localhost:8000/gql || exit 1"
      interval: 60s
      retries: 3
      start_period: 60s
      timeout: 10s
    restart: on-failure:3 # nedojde k restartu pokud je kontejner "unhealthy", maximalne 3 pokusy
    ports:
      - 33012:8000
    depends_on:
      - frontend

  gql_forms:
    image: hrbolek/gql_forms
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=example
      - POSTGRES_HOST=host.docker.internal:5432
      - POSTGRES_DB=data
      - GQLUG_ENDPOINT_URL=http://gql_ug:8000/gql
      - JWTPUBLICKEYURL=http://frontend:8000/oauth/publickey
      - JWTRESOLVEUSERPATHURL=http://frontend:8000/oauth/userinfo
      - DEMO=True
    healthcheck:
      # definice, umoznujici provest test, zda je kontejner v poradku
      test: "curl -f -H 'Content-Type: application/json' -X POST -d '{\"query\":\"query{__schema{types{name}}}\"}' http://localhost:8000/gql || exit 1"
      interval: 60s
      retries: 3
      start_period: 60s
      timeout: 10s
    restart: on-failure:3 # nedojde k restartu pokud je kontejner "unhealthy", maximalne 3 pokusy
    ports:
      - 33013:8000
    depends_on:
      - gql_ug

  frontend:
    image: frontend
    build:
      context: .
    environment:
      - DEMO=False
      - GQL_PROXY=http://apollo:3000/api/gql/
    ports:
      - 33001:8000
    volumes:
    # for development
      - ./server/htmls:/app/server/htmls
```


## Monitoring

Each container emits logs during its life. The logs will be configurable throught `logging.conf` file (see https://docs.python.org/3.10/howto/logging.html).
It is expected that configuration is set to pass log entries into syslon-ng (see https://www.syslog-ng.com/community/b/blog/posts/central-log-server-docker).

Also frontend has measurement of SLA () for prometheus (see https://prometheus.io/). Prometheus is often configured with grafana (see https://grafana.com/).

The proper stack could be (begin of file is missing)

```yaml
  prometheus:
    image: prom/prometheus
    restart: always
    volumes:
      - ./prometheus:/etc/prometheus/
      # - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    ports:
      - 9090:9090
    # links:
    #   - cadvisor:cadvisor
    #   - alertmanager:alertmanager
    # depends_on:
    #   - cadvisor

  grafana:
    image: grafana/grafana
    user: '472'
    restart: always
    environment:
      GF_INSTALL_PLUGINS: 'grafana-clock-panel,grafana-simple-json-datasource'
    # volumes:
    #   - grafana_data:/var/lib/grafana
    #   - ./grafana/provisioning/:/etc/grafana/provisioning/
    # env_file:
    #   - ./grafana/config.monitoring
    ports:
      - 8300:3000
    depends_on:
      - prometheus
```

And content of `/etc/prometheus/prometheus.yml` is

```yaml
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'codelab-monitor'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'uois'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['frontend:8000']
      # - metrics_path: ['/prometheus']
```

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
|        |       |                          |                 |
| AS     |Teacher|                          | 2023/9 - 2024/1 |
| AS     |Teacher| frontend                 | 2023/9 - 2024/1 |
| AS     |Teacher| gql_forms                | 2023/9 - 2024/1 |
|        |       | gql_events               | 2023/9 - 2024/1 |
|        |       | gql_externalids          | 2023/9 - 2024/1 |
|        |       | gql_facilities           | 2023/9 - 2024/1 |
|        |       | gql_granting             | 2023/9 - 2024/1 |
|        |       | gql_publications         | 2023/9 - 2024/1 |
|        |       | gql_lessons              | 2023/9 - 2024/1 |
|        |       | gql_preferences          | 2023/9 - 2024/1 |
|        |       | gql_projects             | 2023/9 - 2024/1 |
|        |       | gql_surveys              | 2023/9 - 2024/1 |
|        |       | gql_ug                   | 2023/9 - 2024/1 |
|        |       | gql_workflow             | 2023/9 - 2024/1 |
|        |       | gql_presences            | 2023/9 - 2024/1 |
|        |       | sql performace measuring | 2023/9 - 2024/1 |


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

It is usefull to create a file per entity. This file should contain also mutations and other specific resolvers.

## Monitoring
There are some libraries, included in Strawberry. Also Prometheus would be taken into account.


## Proper initialization
As the models are not share among gql_s', the order or initializations does not matter.

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


## Run project (just python server)
```bash
uvicorn main:app --port 8000 --env-file environment.txt
```

## Run compose

```yaml
version: "3.9"

services:
  apollo:
    image: hrbolek/apollo_federation
    # image: apollofederation:latest
    environment:
      # promenne, ktere lze cist v kontejneru
      - PORT=3000
      - |
        SERVICES=
        [
          {"name": "ug", "url": "http://gql_ug:8000/gql"},
          {"name": "forms", "url": "http://gql_forms:8000/gql"}
        ]
    healthcheck:
      # definice, umoznujici provest test, zda je kontejner v poradku (vsimnete si portu a srovnejte s portem v environment)
      interval: 60s
      retries: 3
      start_period: 60s
      timeout: 10s
    restart: on-failure:3 # nedojde k restartu pokud je kontejner "unhealthy", maximalne 3 pokusy
    # ports: #v deploymentu by nebylo zadne mapovani portu
      # vnejsi port : port, kde sluzbu poskytuje kontejner
      # - 33000:3000
    depends_on:
      - gql_ug
      - gql_forms

  gql_ug:
    image: hrbolek/gql_ug
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=example
      - POSTGRES_HOST=host.docker.internal:5432
      - POSTGRES_DB=data
      - JWTPUBLICKEYURL=http://frontend:8000/oauth/publickey
      - JWTRESOLVEUSERPATHURL=http://frontend:8000/oauth/userinfo
      - DEMO=True
    healthcheck:
      # definice, umoznujici provest test, zda je kontejner v poradku
      test: "curl -f -H 'Content-Type: application/json' -X POST -d '{\"query\":\"query{__schema{types{name}}}\"}' http://localhost:8000/gql || exit 1"
      interval: 60s
      retries: 3
      start_period: 60s
      timeout: 10s
    restart: on-failure:3 # nedojde k restartu pokud je kontejner "unhealthy", maximalne 3 pokusy
    ports:
      - 33012:8000

  gql_forms:
    image: hrbolek/gql_forms
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=example
      - POSTGRES_HOST=host.docker.internal:5432
      - POSTGRES_DB=data
      - GQLUG_ENDPOINT_URL=http://gql_ug:8000/gql
      - JWTPUBLICKEYURL=http://frontend:8000/oauth/publickey
      - JWTRESOLVEUSERPATHURL=http://frontend:8000/oauth/userinfo
      - DEMO=True
    healthcheck:
      # definice, umoznujici provest test, zda je kontejner v poradku
      test: "curl -f -H 'Content-Type: application/json' -X POST -d '{\"query\":\"query{__schema{types{name}}}\"}' http://localhost:8000/gql || exit 1"
      interval: 60s
      retries: 3
      start_period: 60s
      timeout: 10s
    restart: on-failure:3 # nedojde k restartu pokud je kontejner "unhealthy", maximalne 3 pokusy
    ports:
      - 33013:8000
    depends_on:
      - gql_ug

  frontend:
    image: frontend
    build:
      context: .
    environment:
      - DEMO=False
      - GQL_PROXY=http://apollo:3000/api/gql/
    ports:
      - 33001:8000
    volumes:
    # for development
      - ./server/htmls:/app/server/htmls
```