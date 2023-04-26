import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_forms")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_forms.GraphTypeDefinitions import schema

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

        print(query, flush=True)
        print(variable_values, flush=True)

        resp = await schema.execute(
            query, context_value=context_value, variable_values=variable_values
        )  # , variable_values={"title": "The Great Gatsby"})

        respdata = resp.data[queryEndpoint]
        print(respdata, flush=True)

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
        print(query, flush=True)

        context_value = await createContext(async_session_maker)
        resp = await schema.execute(query, context_value=context_value)

        respdata = resp.data[queryEndpoint]
        print(respdata, flush=True)
        assert resp.errors is None

        datarows = data[tableName]
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

test_reference_forms = createResolveReferenceTest(tableName='forms', gqltype='FormGQLModel')
test_reference_requests = createResolveReferenceTest(tableName='formrequests', gqltype='RequestGQLModel')
test_reference_formtypes = createResolveReferenceTest(tableName='formtypes', gqltype='FormTypeGQLModel')
test_reference_formcategories = createResolveReferenceTest(tableName='formcategories', gqltype='FormCategoryGQLModel')
test_reference_histories = createResolveReferenceTest(tableName='formhistories', gqltype='HistoryGQLModel')
test_reference_sections = createResolveReferenceTest(tableName='formsections', gqltype='SectionGQLModel')
test_reference_parts = createResolveReferenceTest(tableName='formparts', gqltype='PartGQLModel')
test_reference_items = createResolveReferenceTest(tableName='formitems', gqltype='ItemGQLModel')
test_reference_itemtypes = createResolveReferenceTest(tableName='formitemtypes', gqltype='ItemTypeGQLModel')
test_reference_itemcategories = createResolveReferenceTest(tableName='formitemcategories', gqltype='ItemCategoryGQLModel')

test_query_request_by_id = createByIdTest(tableName="formrequests", queryEndpoint="requestById")
test_query_request_page = createPageTest(tableName="formrequests", queryEndpoint="requestsPage")

test_query_form_type_by_id = createByIdTest(tableName="formtypes", queryEndpoint="formTypeById")
test_query_form_type_page = createPageTest(tableName="formtypes", queryEndpoint="formTypePage")
test_query_form_category_by_id = createByIdTest(tableName="formcategories", queryEndpoint="formCategoryById")
test_query_form_category_page = createPageTest(tableName="formcategories", queryEndpoint="formCategoryPage")

test_query_item_by_id = createByIdTest(tableName="formitems", queryEndpoint="itemById")

test_query_item_type_by_id = createByIdTest(tableName="formitemtypes", queryEndpoint="itemTypeById")
test_query_item_type_page = createPageTest(tableName="formitemtypes", queryEndpoint="itemTypePage")
test_query_item_category_by_id = createByIdTest(tableName="formitemcategories", queryEndpoint="itemCategoryById")
test_query_item_category_page = createPageTest(tableName="formitemcategories", queryEndpoint="itemCategoryPage")


@pytest.mark.asyncio
async def test_large_query_1():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['formrequests']
    row = table[0]
    query = 'query{requestById(id: "' + row['id'] + '''") { 
        id
        name
        lastchange
        histories {
            request { id }
            form {
                id
                name
                nameEn
                sections {
                    id
                    name
                    order
                    form { id }
                    parts {
                        id
                        name
                        items {
                            id
                            name
                        }
                    }
                }
                type {
                    id
                    name
                    nameEn
                    category {
                        id
                        name
                        nameEn
                    }
                }

            }
        }
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data
    data = data['requestById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']

@pytest.mark.asyncio
async def test_request_createdby():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['formrequests']
    row = table[0]
    query = 'query{requestById(id: "' + row['id'] + '''") { 
        id
        name
        lastchange
        creator { id }
    }}'''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data
    data = data['requestById']

    print(data, flush=True)
    
    assert resp.errors is None
    assert data['id'] == row['id']

@pytest.mark.asyncio
async def test_large_query():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['formrequests']
    row = table[0]
    user_id = row["createdby"]
    query = '''query($user_id: ID!){
        requestsByCreator(id: $user_id) { 
        id
        lastchange
        creator {
            id
        }
        histories {
            id
            request { id }
            form { id }
        }
    }}'''

    context_value = await createContext(async_session_maker)
    variable_values = {"user_id": user_id}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    print(resp)
    assert resp.errors is None
    data = resp.data
    data = data['requestsByCreator']
    data = data[0]
    #assert False
    #respdata = resp.data['eventById']
    

    assert data['creator']['id'] == row['createdby']


@pytest.mark.asyncio
async def test_resolve_request():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['formrequests']
    row = table[0]

    query = '''
            query {
                _entities(representations: [{ __typename: "RequestGQLModel", id: "''' + row['id'] +  '''" }]) {
                    ...on RequestGQLModel {
                        id
                        lastchange
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data
    print(data, flush=True)
    data = data['_entities'][0]

@pytest.mark.asyncio
async def test_resolve_section():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['formsections']
    row = table[0]

    query = '''
            query {
                _entities(representations: [{ __typename: "SectionGQLModel", id: "''' + row['id'] +  '''" }]) {
                    ...on SectionGQLModel {
                        id
                        lastchange
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data
    print(data, flush=True)
    data = data['_entities'][0]


@pytest.mark.asyncio
async def test_resolve_section():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['formparts']
    row = table[0]

    query = '''
            query {
                _entities(representations: [{ __typename: "PartGQLModel", id: "''' + row['id'] +  '''" }]) {
                    ...on PartGQLModel {
                        id
                        section { id }
                        lastchange
                        order
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    data = resp.data
    print(data, flush=True)
    data = data['_entities'][0]


@pytest.mark.asyncio
async def test_resolve_item():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['formitems']
    row = table[0]

    query = '''
            query {
                _entities(representations: [{ __typename: "ItemGQLModel", id: "''' + row['id'] +  '''" }]) {
                    ...on ItemGQLModel {
                        id
                        part { id }
                        lastchange
                        order
                        name
                        value
                        type { 
                            id
                            category { id }
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






@pytest.mark.asyncio
async def test_reference_history():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['formhistories']
    row = table[0]

    query = '''
            query($id: ID!) {
                _entities(representations: [{ __typename: "HistoryGQLModel", id: $id }]) {
                    ...on HistoryGQLModel {
                        id
                        name
                        lastchange
                        request { id }
                        form { id }
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {'id': row['id']}

    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    print(data, flush=True)
    data = data['_entities'][0]
    assert data['id'] == row['id']



@pytest.mark.asyncio
async def test_reference_user():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['users']
    row = table[0]

    query = '''
            query($id: ID!) {
                _entities(representations: [{ __typename: "UserGQLModel", id: $id }]) {
                    ...on UserGQLModel {
                        id
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {'id': row['id']}

    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    print(data, flush=True)
    data = data['_entities'][0]
    assert data['id'] == row['id']

    
@pytest.mark.asyncio
async def test_requests_by_letters():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['formrequests']
    row = table[0]

    query = '''
            query($letters: String!) {
                requestsByLetters(letters: $letters) {
                    id
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {'letters': row['name'][:4]}

    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    print(data, flush=True)
    data = data['requestsByLetters'][0]
    assert data['id'] == row['id']

@pytest.mark.asyncio
async def test_new_request():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['formtypes']
    row = table[0]

    query = '''
            query($id: ID!) {
                newRequest(formtypeId: $id) {
                    id
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {'id': row['id']}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    print(data, flush=True)
    data = data['newRequest']

    rid = data['id']

    query = '''
            query($id: ID!) {
                requestById(id: $id) {
                    id
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {'id': rid}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    print(data, flush=True)
    assert 'requestById' in data
    data = data['requestById']
    assert data['id'] == rid

    print(data['id'], flush=True)

@pytest.mark.asyncio
async def test_say_hello_forms():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    query = '''
            query($id: ID!) {
                sayHelloForms(id: $id)
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {'id': '132456789'}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data
    print(data, flush=True)
    data = data['sayHelloForms']
    assert 'ello' in data

@pytest.mark.asyncio
async def test_form_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    
    table = data["forms"]
    row = table[0]
    user_id = row["id"]


    name = "form X"
    query = '''
            mutation(
                $name: String!
                
                ) {
                operation: formInsert(form: {
                    name: $name
                    
                }){
                    id
                    msg
                    entity: form {
                        id
                        name
                        lastchange
                    }
                }
            }
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {
        "name": name
    }
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    
    print(resp, flush=True)

    assert resp.errors is None
    data = resp.data['operation']
    assert data["msg"] == "ok"
    data = data["entity"]
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
                operation: formUpdate(form: {
                id: $id
                lastchange: $lastchange
                name: $name
            }){
                id
                msg
                entity: form {
                    name
                    id
                    lastchange
                }
            }
            }
        '''
    newName = "newName"
    context_value = await createContext(async_session_maker)
    variable_values = {"id": id, "name": newName, "lastchange": lastchange}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None

    data = resp.data['operation']
    assert data['msg'] == "ok"
    data = data["entity"]
    assert data["name"] == newName

    # lastchange je jine, musi fail
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    data = resp.data['operation']
    assert data['msg'] == "fail"

    pass
