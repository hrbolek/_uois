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

    groupid = data['events_groups'][0]['group_id']

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
    respdata = resp.data['_entities']
    assert respdata[0]['id'] == groupid
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
    respdata = resp.data['eventByGroup']
    assert respdata[0]['id'] == row['event_id']
    assert resp.errors is None

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
                    editor {
                        id
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    print(resp, flush=True)
    respdata = resp.data['eventByUser']
    assert respdata[0]['id'] == row['event_id']
    assert resp.errors is None


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

@pytest.mark.asyncio
async def test_event_editor():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    id = data['events'][0]['id']
    print(id, flush=True)
    query = '''
            query {
                _entities(representations: [{ __typename: "EventEditorGQLModel", id: "''' + id +  '''" }]) {
                    ...on EventEditorGQLModel {
                        id
                        result
                        event { id }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    print(resp, flush=True)
    respdata = resp.data['_entities']
    print(respdata, flush=True)
    assert respdata[0]['id'] == id
    assert resp.errors is None