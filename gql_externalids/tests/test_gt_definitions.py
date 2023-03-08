import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_externalids")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_externalids.GraphTypeDefinitions import schema

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
    
#test_query_externalids_by_id = createByIdTest(tableName="externalids", queryEndpoint="eventById")
#test_query_externalidtypes_by_id = createByIdTest(tableName="externalidtypes", queryEndpoint="eventTypeById")


@pytest.mark.asyncio
async def test_external_ids():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['externalids']
    row = table[0]
    query = 'query{externalIds(internalId: "' + row['inner_id'] + '''") { 
        id
        innerId
        outerId
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data

    #respdata = resp.data['eventById']
    assert resp.errors is None

    assert data['externalIds'][0]['innerId'] == row['inner_id']
    assert data['externalIds'][0]['outerId'] == row['outer_id']


@pytest.mark.asyncio
async def test_internal_ids():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['externalids']
    row = table[0]
    print(row, flush=True)
    query = 'query{internalId(externalId: "' + row['outer_id'] + f'''", externalTypeId: "{row['typeid_id']}")''' + '''}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data
    print(data, flush=True)
    #respdata = resp.data['eventById']
    assert resp.errors is None

    assert data['internalId'] == row['inner_id']



@pytest.mark.asyncio
async def test_representation_externalid():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    id = data['externalids'][0]['id']

    query = '''
            query {
                _entities(representations: [{ __typename: "ExternalIdGQLModel", id: "''' + id +  '''" }]) {
                    ...on ExternalIdGQLModel {
                        id
                        innerId
                        outerId
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
async def test_representation_user_editor():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    id = data['externalids'][0]['inner_id']

    query = '''
            query {
                _entities(representations: [{ __typename: "UserEditorGQLModel", id: "''' + id +  '''" }]) {
                    ...on UserEditorGQLModel {
                        id
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
async def test_representation_user():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['users']
    row = table[0]
    id = row['id']

    query = '''
            query {
                _entities(representations: [{ __typename: "UserGQLModel", id: "''' + id +  '''" }]) {
                    ...on UserGQLModel {
                        id
                        externalIds {
                            innerId
                            outerId
                            idType {id name}
                            typeName
                        }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    print(resp, flush=True)
    respdata = resp.data['_entities']
    assert respdata[0]['externalIds'][0]['innerId'] == row['id']
    assert resp.errors is None

@pytest.mark.asyncio
async def test_representation_group():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['groups']
    row = table[0]
    id = row['id']

    query = '''
            query {
                _entities(representations: [{ __typename: "GroupGQLModel", id: "''' + id +  '''" }]) {
                    ...on GroupGQLModel {
                        id
                        externalIds {
                            innerId
                            outerId
                            idType {id name}
                            typeName
                        }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    print(resp, flush=True)
    respdata = resp.data['_entities']
    assert respdata[0]['externalIds'][0]['innerId'] == row['id']
    assert resp.errors is None


@pytest.mark.asyncio
async def test_group_add_external_id():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['groups']
    row = table[0]
    id = row['id']

    query = '''
            query($id: ID!, $externalId: String!, $typeidId: ID!) {
                _entities(representations: [{ __typename: "GroupEditorGQLModel", id: $id }]) {
                    ...on GroupEditorGQLModel {
                        id
                        assignExternalId(externalId: $externalId, typeidId: $typeidId) {
                            id
                        }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {'id': id, 'externalId': '999', 'typeidId': data['externalidtypes'][0]['id']}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None

    query = '''
            query($id: ID!) {
                _entities(representations: [{ __typename: "GroupGQLModel", id: $id }]) {
                    ...on GroupGQLModel {
                        id
                        externalIds {
                            innerId
                            outerId
                            idType {id name}
                            typeName
                        }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {'id': id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    print(resp, flush=True)

    assert resp.errors is None
    respdata = resp.data['_entities']
    eids = list(map(lambda item: item['outerId'], respdata[0]['externalIds']))
    
    assert '999' in eids

@pytest.mark.asyncio
async def test_user_add_external_id():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['groups']
    row = table[0]
    id = row['id']

    query = '''
            query($id: ID!, $externalId: String!, $typeidId: ID!) {
                _entities(representations: [{ __typename: "UserEditorGQLModel", id: $id }]) {
                    ...on UserEditorGQLModel {
                        id
                        assignExternalId(externalId: $externalId, typeidId: $typeidId) {
                            id
                        }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {'id': id, 'externalId': '999', 'typeidId': data['externalidtypes'][0]['id']}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None

    query = '''
            query($id: ID!) {
                _entities(representations: [{ __typename: "UserGQLModel", id: $id }]) {
                    ...on UserGQLModel {
                        id
                        externalIds {
                            innerId
                            outerId
                            idType {id name}
                            typeName
                        }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {'id': id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    print(resp, flush=True)

    assert resp.errors is None
    respdata = resp.data['_entities']
    eids = list(map(lambda item: item['outerId'], respdata[0]['externalIds']))
    
    assert '999' in eids

