import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append('../gql_ug')

import pytest 
#from ..uoishelpers.uuid import UUIDColumn

from gql_ug.GraphTypeDefinitions import schema

from shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata, createContext



def createByIdTest(tableName, queryEndpoint, attributeNames=['id', 'name']):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)
        
        data = get_demodata()
        datarow = data[tableName][0]

        query = ("query($id: ID!){" 
            f"{queryEndpoint}(id: $id)" 
            "{ id, name }}")

        context_value = await createContext(async_session_maker)
        variable_values = {
            'id': datarow['id']
        }
        resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)#, variable_values={"title": "The Great Gatsby"})
        
        respdata = resp.data[queryEndpoint]

        assert resp.errors is None

        for att in attributeNames:
            assert respdata[att] == datarow[att] 

    return result_test


def createPageTest(tableName, queryEndpoint, attributeNames=['id', 'name']):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)
        
        data = get_demodata()

        query = ("query{" 
            f"{queryEndpoint}" 
            "{ id, name }}")

        context_value = await createContext(async_session_maker)
        resp = await schema.execute(query, context_value=context_value)
        
        respdata = resp.data[queryEndpoint]
        datarows = data[tableName]

        assert resp.errors is None

        for rowa, rowb in zip(respdata, datarows):
            for att in attributeNames:
                assert rowa[att] == rowb[att] 

    return result_test



test_query_user_by_id = createByIdTest(tableName='users', queryEndpoint='userById')
test_query_group_by_id = createByIdTest(tableName='groups', queryEndpoint='groupById')
test_query_grouptype_by_id = createByIdTest(tableName='grouptypes', queryEndpoint='groupTypeById')
test_query_roletype_by_id = createByIdTest(tableName='roletypes', queryEndpoint='roleTypeById')

test_query_user_page = createPageTest(tableName='users', queryEndpoint='userPage')
test_query_group_page = createPageTest(tableName='groups', queryEndpoint='groupPage')
test_query_grouptype_page = createPageTest(tableName='grouptypes', queryEndpoint='groupTypePage')
test_query_roletype_page = createPageTest(tableName='roletypes', queryEndpoint='roleTypePage')


@pytest.mark.asyncio
async def test_large_query():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)
    
    data = get_demodata()

    query = """query {
         groupById(id: "2d9dcd22-a4a2-11ed-b9df-0242ac120003") {
            id
            name
            roles {
            user {
                id
                name
                surname
                email
            }
            roletype {
                id
                name
            }
            }
            subgroups {
            id
            name
            }
            memberships {
            user {
                id
                name
                
                roles {
                roletype {
                    id
                    name
                }
                group {
                    id
                    name
                }
                }
                
                membership {
                group {
                    id
                    name
                }
                }
            }
            }
        }
        }"""


    context_value = await createContext(async_session_maker)
    resp = await schema.execute(query, context_value=context_value)
    
    respdata = resp.data['groupById']

    assert resp.errors is None
    assert respdata['id'] == '2d9dcd22-a4a2-11ed-b9df-0242ac120003'

