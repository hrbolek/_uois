import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_workflow.GraphTypeDefinitions import schema

from tests.shared import (
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
        assert resp.errors is None

        respdata = resp.data[queryEndpoint]
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

# test_query_user_by_id = createByIdTest(tableName="users", queryEndpoint="userById")
# test_query_group_by_id = createByIdTest(tableName="groups", queryEndpoint="groupById")
# test_query_grouptype_by_id = createByIdTest(
#     tableName="grouptypes", queryEndpoint="groupTypeById"
# )
# test_query_roletype_by_id = createByIdTest(
#     tableName="roletypes", queryEndpoint="roleTypeById"
# )

# test_query_user_page = createPageTest(tableName="users", queryEndpoint="userPage")
# test_query_group_page = createPageTest(tableName="groups", queryEndpoint="groupPage")
# test_query_grouptype_page = createPageTest(
#     tableName="grouptypes", queryEndpoint="groupTypePage"
# )
# test_query_roletype_page = createPageTest(
#     tableName="roletypes", queryEndpoint="roleTypePage"
# )


# test_reference_user = createResolveReferenceTest(tableName="users", gqltype="UserGQLModel")
# test_reference_group = createResolveReferenceTest(tableName="groups", gqltype="GroupGQLModel")
# test_reference_group_type = createResolveReferenceTest(tableName="grouptypes", gqltype="GroupTypeGQLModel")
# test_reference_role = createResolveReferenceTest(tableName="roles", gqltype="RoleGQLModel")
# test_reference_role_type = createResolveReferenceTest(tableName="roletypes", gqltype="RoleTypeGQLModel")
# test_reference_membership = createResolveReferenceTest(tableName="memberships", gqltype="MembershipGQLModel")

test_reference_workflow = createResolveReferenceTest(tableName="awworkflows", gqltype="WorkflowGQLModel")
test_query_workflow_by_id = createByIdTest(tableName="awworkflows", queryEndpoint="workflowById")
test_query_workflow_page = createPageTest(tableName="awworkflows", queryEndpoint="workflowPage")

@pytest.mark.asyncio
async def test_workflow_mutation():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    
    table = data["awworkflows"]
    row = table[0]
    user_id = row["id"]


    name = "workflow X"
    query = '''
            mutation(
                $name: String!
                
                ) {
                operation: workflowInsert(workflow: {
                    name: $name
                    
                }){
                    id
                    msg
                    entity: workflow {
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
                operation: workflowUpdate(workflow: {
                id: $id,
                lastchange: $lastchange
                name: $name
            }){
                id
                msg
                entity: workflow {
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
