import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_facilities")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_facilities.GraphTypeDefinitions import schema

from shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
)


def createByIdTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    attlist = ' '.join(attributeNames)
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        assert data.get(tableName, None) is not None
        datatable = data[tableName]
        assert len(datatable) > 0
        datarow = data[tableName][0]

        query = "query($id: ID!){" f"{queryEndpoint}(id: $id)" "{" + attlist + "}}"

        context_value = await createContext(async_session_maker)
        variable_values = {"id": datarow["id"]}
        print("createByIdTest", queryEndpoint, variable_values, flush=True)
        resp = await schema.execute(
            query, context_value=context_value, variable_values=variable_values
        )  # , variable_values={"title": "The Great Gatsby"})

        respdata = resp.data[queryEndpoint]

        assert resp.errors is None
        assert respdata is not None

        for att in attributeNames:
            assert respdata[att] == datarow[att]

    return result_test


def createPageTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    attlist = ' '.join(attributeNames)
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()

        query = "query{" f"{queryEndpoint}" "{" + attlist + "}}"

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
    attlist = ' '.join(attributeNames)
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        table = data[tableName]
        for row in table:
            rowid = row['id']

            query = (
                'query { _entities(representations: [{ __typename: '+ f'"{gqltype}", id: "{rowid}"' + 
                ' }])' +
                '{' +
                f'...on {gqltype}' + 
                '{' +
                  attlist + '}'+
                '}' + 
                '}')

            context_value = await createContext(async_session_maker)
            resp = await schema.execute(query, context_value=context_value)
            data = resp.data
            print(data, flush=True)
            data = data['_entities'][0]

            assert data['id'] == rowid

    return result_test

    
test_query_facilities_by_id = createByIdTest(tableName="facilities", queryEndpoint="facilityById")
test_query_facilitytypes_by_id = createByIdTest(tableName="facilitytypes", queryEndpoint="facilityTypeById")

test_query_facilitytypes_page = createPageTest(tableName="facilitytypes", queryEndpoint="facilityTypePage")
test_query_facilityeventstatetypes_page = createPageTest(tableName="facilityeventstatetypes", queryEndpoint="facilityEventStateTypePage")



@pytest.mark.asyncio
async def test_large_query():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['facilities']
    row = table[0]
    id = row["id"]
    query = '''query($id: ID!){
        facilityById(id: $id) { 
            id
            name
            label
            lastchange
            address
            valid
            capacity
            geometry
            geolocation
            masterFacility { id }
            group { id }
            type {
                id
                name
                nameEn
            }
            subFacilities {
                id
                name
                nameEn
                masterFacility { id }
            }
            eventStates {
                id
                event { id }
                state { id name nameEn}
                facility { id }
            }
    }}'''

    context_value = await createContext(async_session_maker)
    variable_values={"id": id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    print(resp, flush=True)
    assert resp.errors is None
    data = resp.data
    assert data is not None
    data = data['facilityById']
    #assert False
    #respdata = resp.data['eventById']

    assert data['id'] == id
    #assert data['masterFacility']['id'] == row['master_facility_id']

    print(data, flush=True)
    print(data['eventStates'], flush=True)
    if len(data['eventStates']) > 0:
        assert data['eventStates'][0]['facility']['id'] == row['id']



@pytest.mark.asyncio
async def test_large_page_query():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['facilities']
    row = table[0]
    query = '''query{facilityPage { 
        id
        name
        label
        lastchange
        address
        valid
        capacity
        geometry
        geolocation
        masterFacility { id }
        group { id }
        type {
            id
            name
            nameEn
        }
        subFacilities {
            id
            name
            nameEn
            masterFacility { id }
        }
        eventStates {
            id
            event { id }
            state { id name nameEn}
            facility { id }
        }
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    print(resp, flush=True)
    assert resp.errors is None
    data = resp.data
    assert data is not None
    data = data['facilityPage'][0]
    #assert False
    #respdata = resp.data['eventById']
    assert resp.errors is None

    assert data['id'] == row['id']

    print(data, flush=True)
    #print(data['eventStates'], flush=True)
    #assert data['eventStates'][0]['facility']['id'] == row['id']


@pytest.mark.asyncio
async def test_group_facilities():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['facilities']
    row = table[0]

    query = '''
            query {
                _entities(representations: [{ __typename: "GroupGQLModel", id: "''' + row['group_id'] +  '''" }]) {
                    ...on GroupGQLModel {
                        id
                        facilities {
                            id
                        }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data
    print(data, flush=True)
    data = data['_entities'][0]

    facilityids = list(map(lambda item: item['id'], data['facilities']))
    assert row['id'] in facilityids


@pytest.mark.asyncio
async def test_say_hello():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['facilities']
    row = table[0]
    query = 'query{sayHelloFacility(id: "' + row['id'] + '''") 
    }'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data
    #print(resp, flush=True)
    data = data['sayHelloFacility']

    #respdata = resp.data['eventById']
    assert resp.errors is None

    assert 'ello' in data


@pytest.mark.asyncio
async def test_representation_event():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    id = data['events'][0]['id']

    query = '''
            query {
                _entities(representations: [{ __typename: "EventGQLModel", id: "''' + id +  '''" }]) {
                    ...on EventGQLModel {
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
async def test_representation_facility_event():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    id = data['facilities_events'][0]['id']

    query = '''
            query {
                _entities(representations: [{ __typename: "FacilityEventGQLModel", id: "''' + id +  '''" }]) {
                    ...on FacilityEventGQLModel {
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
async def test_representation_group():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    id = data['groups'][0]['id']

    query = '''
            query {
                _entities(representations: [{ __typename: "GroupGQLModel", id: "''' + id +  '''" }]) {
                    ...on GroupGQLModel {
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
async def test_representation_facility_state_type():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()

    id = data['facilityeventstatetypes'][0]['id']

    query = '''
            query {
                _entities(representations: [{ __typename: "FacilityEventStateTypeGQLModel", id: "''' + id +  '''" }]) {
                    ...on FacilityEventStateTypeGQLModel {
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


# @pytest.mark.asyncio
# async def test_external_ids():
#     async_session_maker = await prepare_in_memory_sqllite()
#     await prepare_demodata(async_session_maker)

#     data = get_demodata()
#     table = data['externalids']
#     row = table[0]
#     query = 'query{externalIds(internalId: "' + row['inner_id'] + '''") { 
#         id
#         innerId
#         outerId
#     }}'''

#     context_value = await createContext(async_session_maker)
#     resp = await schema.execute(query, context_value=context_value)
#     data = resp.data

#     #respdata = resp.data['eventById']
#     assert resp.errors is None

#     assert data['externalIds'][0]['innerId'] == row['inner_id']
#     assert data['externalIds'][0]['outerId'] == row['outer_id']


# @pytest.mark.asyncio
# async def test_representation_externalid():
#     async_session_maker = await prepare_in_memory_sqllite()
#     await prepare_demodata(async_session_maker)

#     data = get_demodata()

#     id = data['externalids'][0]['id']

#     query = '''
#             query {
#                 _entities(representations: [{ __typename: "ExternalIdGQLModel", id: "''' + id +  '''" }]) {
#                     ...on ExternalIdGQLModel {
#                         id
#                         innerId
#                         outerId
#                     }
#                 }
#             }
#         '''

#     context_value = await createContext(async_session_maker)
#     resp = await schema.execute(query, context_value=context_value)
    
#     print(resp, flush=True)
#     respdata = resp.data['_entities']
#     assert respdata[0]['id'] == id
#     assert resp.errors is None

    
@pytest.mark.asyncio
async def test_facility_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    
    table = data["facilities"]
    row = table[0]
    id = row["id"]

    table = data["facilitytypes"]
    row = table[0]
    facilitytype_id = row["id"]


    name = "Facility X"
    query = '''
            mutation(
                $name: String!,
                $facilitytype_id: ID!
                ) {
                operation: facilityInsert(facility: {
                    name: $name,
                    facilitytypeId: $facilitytype_id
                }){
                    id
                    msg
                    entity: facility {
                        id
                        name
                        lastchange
                        type { id }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {
        "name": name,
        "facilitytype_id": facilitytype_id
    }
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    
    print(resp, flush=True)

    assert resp.errors is None
    data = resp.data['operation']
    assert data["msg"] == "ok"
    data = data["entity"]
    assert data["type"]["id"] == facilitytype_id
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
                operation: facilityUpdate(facility: {
                id: $id,
                lastchange: $lastchange
                name: $name
            }){
                id
                msg
                entity: facility {
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
