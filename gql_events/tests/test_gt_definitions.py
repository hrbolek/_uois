import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_events")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_events.GraphTypeDefinitions import schema

from shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
)


def createByIdTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        datarow = data[tableName][0]

        query = "query($id: ID!){" f"{queryEndpoint}(id: $id)" "{ id, name }}"

        context_value = await createContext(async_session_maker)
        variable_values = {"id": datarow["id"]}
        resp = await schema.execute(
            query, context_value=context_value, variable_values=variable_values
        )  # , variable_values={"title": "The Great Gatsby"})

        respdata = resp.data[queryEndpoint]

        assert resp.errors is None

        for att in attributeNames:
            assert respdata[att] == datarow[att]

    return result_test


def createPageTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()

        query = "query{" f"{queryEndpoint}" "{ id, name }}"

        context_value = await createContext(async_session_maker)
        resp = await schema.execute(query, context_value=context_value)

        respdata = resp.data[queryEndpoint]
        datarows = data[tableName]

        assert resp.errors is None

        for rowa, rowb in zip(respdata, datarows):
            for att in attributeNames:
                assert rowa[att] == rowb[att]

    return result_test

def createResolveReferenceTest(tableName, gqltype, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()

        data = get_demodata()
        table = data[tableName]
        for row in table:
            rowid = row['id']

            query = (
                'query { _entities(representations: [{ __typename: '+ f'"{gqltype}", id: "{rowid}"' + 
                ' }])' +
                '{' +
                f'...on {gqltype}' + 
                '{ id }'+
                '}' + 
                '}')

            context_value = await createContext(async_session_maker)
            resp = await schema.execute(query, context_value=context_value)
            data = resp.data
            print(data, flush=True)
            data = data['_entities'][0]

            assert data['id'] == rowid

    return result_test

test_query_event_by_id = createByIdTest(tableName="events", queryEndpoint="eventById")
test_query_eventtype_by_id = createByIdTest(tableName="eventtypes", queryEndpoint="eventTypeById")


@pytest.mark.asyncio
async def test_large_query():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    events = data['events']
    event0 = events[0]
    query = 'query{eventById(id: "' + event0['id'] + '''") { 
        id
        name
        startdate
        enddate
        presences { 
            id
            user { id }
            presenceType { 
                id
                name
            }
            invitationType { 
                id
                name
            }
        }
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    #respdata = resp.data['eventById']

    assert resp.errors is None


@pytest.mark.asyncio
async def test_large_query_2():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    query = '''query{eventTypeById(id: "b87d3ff0-8fd4-11ed-a6d4-0242ac110002") { 
        id
        name
        events {
            name
            startdate
            enddate
            eventType {
                id
                name
                nameEn
            }
            presences(invitationTypes: ["e871403c-a79c-11ed-b76e-0242ac110002"]) { 
                id
                user { id }
                presenceType { 
                    id
                    name
                    nameEn
                }
                invitationType { 
                    id
                    name
                    nameEn
                }
            }
            groups { id }
        }
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    #respdata = resp.data['eventById']

    assert resp.errors is None

@pytest.mark.asyncio
async def test_large_user():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    userid = data['events_users'][0]['user_id']

    query = '''
            query {
                _entities(representations: [{ __typename: "UserGQLModel", id: "''' + userid +  '''" }]) {
                    ...on UserGQLModel {
                        id
                        events {
                            id
                        }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    print(resp, flush=True)
    respdata = resp.data['_entities']
    assert respdata[0]['id'] == userid
    assert resp.errors is None

@pytest.mark.asyncio
async def test_large_group():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    table = data['events_groups']
    row = table[0]
    groupid = row['group_id']

    query = '''
            query {
                _entities(representations: [{ __typename: "GroupGQLModel", id: "''' + groupid +  '''" }]) {
                    ...on GroupGQLModel {
                        id
                        events {
                            id
                        }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    print(resp, flush=True)
    assert resp.errors is None
    
    respdata = resp.data['_entities']
    assert respdata[0]['id'] == groupid
    


@pytest.mark.asyncio
async def test_large_user():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    userid = data['events_users'][0]['user_id']

    query = '''
            query {
                _entities(representations: [{ __typename: "UserGQLModel", id: "''' + userid +  '''" }]) {
                    ...on UserGQLModel {
                        id
                        events {
                            id
                        }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    print(resp, flush=True)
    respdata = resp.data['_entities']
    assert respdata[0]['id'] == userid
    assert resp.errors is None

@pytest.mark.asyncio
async def test_presence_resolve():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    id = data['events_users'][0]['id']

    query = '''
            query {
                _entities(representations: [{ __typename: "PresenceGQLModel", id: "''' + id +  '''" }]) {
                    ...on PresenceGQLModel {
                        id
                        event {
                            id
                        }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    print(resp, flush=True)
    respdata = resp.data['_entities']
    assert respdata[0]['id'] == id
    assert resp.errors is None

@pytest.mark.asyncio
async def test_event_by_group():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    row = data['events_groups'][0]
    id = row['group_id']

    query = '''
            query {
                eventByGroup(id: "''' + id +  '''", startdate: "2000-01-01", enddate: "2199-12-31") {
                    id
                    name
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    print(resp, flush=True)
    assert resp.errors is None
    respdata = resp.data['eventByGroup']
    assert respdata[0]['id'] == row['event_id']
    

@pytest.mark.asyncio
async def test_event_by_user():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    row = data['events_users'][0]
    id = row['user_id']

    query = '''
            query {
                eventByUser(id: "''' + id +  '''", startdate: "2000-01-01", enddate: "2199-12-31") {
                    id
                    name
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    print(resp, flush=True)
    assert resp.errors is None

    respdata = resp.data['eventByUser']
    assert respdata[0]['id'] == row['event_id']


@pytest.mark.asyncio
async def test_event_page():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    row = data['events'][0]

    query = '''
            query {
                eventPage {
                    id
                    name
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    print(resp, flush=True)
    respdata = resp.data['eventPage']
    assert len(respdata) == len(data['events'])
    assert respdata[0]['id'] == row['id']
    assert resp.errors is None



@pytest.mark.asyncio
async def test_event_type_page():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    row = data['eventtypes'][0]

    query = '''
            query {
                eventTypePage(skip: 0, limit: 100) {
                    id
                    name
                    nameEn
                }
                sayHelloEvents(id: "42")
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    print(resp, flush=True)
    respdata = resp.data['eventTypePage']
    assert len(respdata) == len(data['eventtypes'])
    assert respdata[0]['id'] == row['id']
    assert resp.errors is None

# @pytest.mark.asyncio
# async def test_event_editor():
#     async_session_maker = await prepare_in_memory_sqllite()
#     await prepare_demodata(async_session_maker)

#     data = get_demodata()

#     id = data['events'][0]['id']
#     print(id, flush=True)
#     query = '''
#             query {
#                 _entities(representations: [{ __typename: "EventEditorGQLModel", id: "''' + id +  '''" }]) {
#                     ...on EventEditorGQLModel {
#                         id
#                         result
#                         event { id }
#                     }
#                 }
#             }
#         '''

#     context_value = await createContext(async_session_maker)
#     resp = await schema.execute(query, context_value=context_value)   
#     print(resp, flush=True)
#     assert resp.errors is None

#     respdata = resp.data['_entities']
#     print(respdata, flush=True)
#     assert respdata[0]['id'] == id

    
@pytest.mark.asyncio
async def test_event_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    
    table = data["events"]
    row = table[0]
    id = row["id"]

    table = data["eventtypes"]
    row = table[0]
    eventtype_id = row["id"]


    name = "Event X"
    query = '''
            mutation(
                $name: String!,
                $eventtype_id: ID!
                ) {
                operation: eventInsert(event: {
                    name: $name,
                    eventtypeId: $eventtype_id
                }){
                    id
                    msg
                    entity: event {
                        id
                        name
                        lastchange
                        eventType { id }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {
        "name": name,
        "eventtype_id": eventtype_id
    }
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    
    print(resp, flush=True)

    assert resp.errors is None
    data = resp.data['operation']
    assert data["msg"] == "ok"
    data = data["entity"]
    assert data["eventType"]["id"] == eventtype_id
    assert data["name"] == name
    #assert data["name"] == name
    
   
    id = data["id"]
    lastchange = data["lastchange"]
    name = "NewName"
    query = '''
            mutation(
                $id: ID!,
                $lastchange: DateTime!
                $name: String!
                ) {
                operation: eventUpdate(event: {
                id: $id,
                lastchange: $lastchange
                name: $name
            }){
                id
                msg
                entity: event {
                    id
                    name
                    lastchange
                }
            }
            }
        '''
    order = 2
    context_value = await createContext(async_session_maker)
    variable_values = {"id": id, "name": name, "lastchange": lastchange}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None

    data = resp.data['operation']
    assert data['msg'] == "ok"
    data = data["entity"]
    assert data["name"] == name

    # lastchange je jine, musi fail
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data['operation']
    assert data['msg'] == "fail"

    pass
