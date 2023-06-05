import sqlalchemy
import sys
import asyncio

# setting path
#sys.path.append("../gql_granting")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_lessons.GraphTypeDefinitions import schema

from tests.shared import (
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
        print(resp, flush=True)
        assert resp.errors is None

        respdata = resp.data[queryEndpoint]

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
        print(resp, flush=True)
        assert resp.errors is None

        respdata = resp.data[queryEndpoint]
        datarows = data[tableName]

        

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

test_query_lessons_by_id = createByIdTest(tableName="plan_lessons", queryEndpoint="plannedLessonById")
#test_query_lessons_page = createPageTest(tableName="plan_lessons", queryEndpoint="plannedLessonPage")

@pytest.mark.asyncio
async def test_planned_lesson_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    
    table = data["plan_lessons"]
    row = table[0]
    id = row["id"]


    name = "lesson X"
    query = '''
            mutation(
                
                $name: String!
                ) {
                operation: plannedLessonInsert(lesson: {
                    name: $name
                }){
                    id
                    msg
                    entity: lesson {
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
                operation: plannedLessonUpdate(lesson: {
                id: $id,
                lastchange: $lastchange
                name: $name
            }){
                id
                msg
                entity: lesson {
                    id
                    name
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

@pytest.mark.asyncio
async def _test_planned_lesson_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    
    table = data["plan_lessons"]
    row = table[0]
    id = row["id"]


    name = "lesson X"
    query = '''
{
  __schema {
    types {
      name
    fields {
      name
      type {
        name
        kind
      }
    }
    }
  }
}
        '''

    context_value = await createContext(async_session_maker)
    variable_values = {    }
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    
    print(resp, flush=True)
    assert False

    pass

@pytest.mark.asyncio
async def test_planned_lesson_group_delete():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    
    table = data["plan_lessons_groups"]
    row = table[0]

    query = """mutation($group_id: ID! $lesson_id: ID!) {
        result: plannedLessonGroupDelete(
            grouplesson: {groupId: $group_id, planlessonId: $lesson_id }) {
            id
            msg
            lesson {
            plan {
                __typename
                id
                lastchange
                lessons {
                    __typename
                    id
                    name
                    users {
                    __typename
                    id
                    }
                    groups {
                    __typename
                    id
                    }
                    facilities {
                    __typename
                    id
                    }
                }
            }
            }
        }
        }"""

    context_value = await createContext(async_session_maker)
    variable_values = {
        "group_id": row["group_id"],
        "lesson_id": row["planlesson_id"]
        }
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    assert resp.data is not None

    print(resp.data, flush=True)

    data = resp.data
    msg = data["result"]["msg"]
    assert msg == "ok"

@pytest.mark.asyncio
async def test_planned_lesson_user_delete():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    
    table = data["plan_lessons_users"]
    row = table[0]

    query = """mutation($user_id: ID! $lesson_id: ID!) {
        result: plannedLessonUserDelete(
            userlesson: {userId: $user_id, planlessonId: $lesson_id }) {
            id
            msg
            lesson {
                users {
                    __typename
                    id
                }
            }
        }
    }"""

    context_value = await createContext(async_session_maker)
    variable_values = {
        "user_id": row["user_id"],
        "lesson_id": row["planlesson_id"]
        }
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    assert resp.data is not None

    print(resp.data, flush=True)

    data = resp.data
    msg = data["result"]["msg"]
    assert msg == "ok"

    users = data["result"]["lesson"]["users"]
    userids = list(map(lambda item: item["id"], users))
    assert row["user_id"] not in userids
