import sqlalchemy
import asyncio
import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_ug.GraphTypeDefinitions import schema

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

test_query_user_by_id = createByIdTest(tableName="users", queryEndpoint="userById")
test_query_group_by_id = createByIdTest(tableName="groups", queryEndpoint="groupById")
test_query_grouptype_by_id = createByIdTest(
    tableName="grouptypes", queryEndpoint="groupTypeById"
)
test_query_roletype_by_id = createByIdTest(
    tableName="roletypes", queryEndpoint="roleTypeById"
)

test_query_user_page = createPageTest(tableName="users", queryEndpoint="userPage")
test_query_group_page = createPageTest(tableName="groups", queryEndpoint="groupPage")
test_query_grouptype_page = createPageTest(
    tableName="grouptypes", queryEndpoint="groupTypePage"
)
test_query_roletype_page = createPageTest(
    tableName="roletypes", queryEndpoint="roleTypePage"
)


test_reference_user = createResolveReferenceTest(tableName="users", gqltype="UserGQLModel")
test_reference_group = createResolveReferenceTest(tableName="groups", gqltype="GroupGQLModel")
test_reference_group_type = createResolveReferenceTest(tableName="grouptypes", gqltype="GroupTypeGQLModel")
test_reference_role = createResolveReferenceTest(tableName="roles", gqltype="RoleGQLModel")
test_reference_role_type = createResolveReferenceTest(tableName="roletypes", gqltype="RoleTypeGQLModel")
test_reference_membership = createResolveReferenceTest(tableName="memberships", gqltype="MembershipGQLModel")


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

    respdata = resp.data["groupById"]

    assert resp.errors is None
    assert respdata["id"] == "2d9dcd22-a4a2-11ed-b9df-0242ac120003"

@pytest.mark.asyncio
async def test_query_user():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['users']

    for row in table:
        

        query = """query($id: ID!) {
            userById(id: $id) {
                id
                name
                surname
                email

                editor { id }

                lastchange
                roles {
                    id
                }
            }
            }"""

        context_value = await createContext(async_session_maker)
        variable_values = {"id": row["id"]}
        resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

        respdata = resp.data["userById"]

        assert resp.errors is None
        assert respdata["id"] == row["id"]

@pytest.mark.asyncio
async def test_query_group():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['groups']

    for row in table:
        

        query = """query($id: ID!) {
            groupById(id: $id) {
                id
                name
                editor { id }

                lastchange
                valid

                grouptype { id }
                mastergroup { id }
            }
            }"""

        context_value = await createContext(async_session_maker)
        variable_values = {"id": row["id"]}
        resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

        respdata = resp.data["groupById"]

        assert resp.errors is None
        assert respdata["id"] == row["id"]

@pytest.mark.asyncio
async def test_query_group_roles():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['groups']

    for row in table:
        

        query = """query($id: ID!) {
            groupById(id: $id) {
                id
                roles { 
                    id
                    startdate
                    enddate
                    valid
                    group { id }
                    user { id }
                    roletype {
                        id
                        name
                    }
                }
            }
            }"""

        context_value = await createContext(async_session_maker)
        variable_values = {"id": row["id"]}
        resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

        respdata = resp.data["groupById"]

        assert resp.errors is None
        assert respdata["id"] == row["id"]

@pytest.mark.asyncio
async def test_query_role_type():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['roletypes']

    for row in table:
        query = """query($id: ID!) {
            roleTypeById(id: $id) {
                id
                name
                nameEn
                roles { 
                    id
                    startdate
                    enddate
                    valid
                }
            }
            }"""

        context_value = await createContext(async_session_maker)
        variable_values = {"id": row["id"]}
        resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

        respdata = resp.data["roleTypeById"]

        assert resp.errors is None
        assert respdata["id"] == row["id"]
        assert respdata["name"] == row["name"]

@pytest.mark.asyncio
async def test_query_group_type():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['grouptypes']

    for row in table:
        query = """query($id: ID!) {
            groupTypeById(id: $id) {
                id
                name
                nameEn
                groups { 
                    id
                }
            }
            }"""

        context_value = await createContext(async_session_maker)
        variable_values = {"id": row["id"]}
        resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

        respdata = resp.data["groupTypeById"]

        assert resp.errors is None
        assert respdata["id"] == row["id"]
        assert respdata["name"] == row["name"]


@pytest.mark.asyncio
async def test_query_group_editor_add_member():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['groups']
    row = table[0]
    query = """query($id: ID!) {
        groupById(id: $id) {
            memberships {
                user { id }
            }
            editor{
                id
            }
            id
        }
        }"""

    context_value = await createContext(async_session_maker)
    variable_values = {"id": row["id"]}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

    respdata = resp.data["groupById"]

    assert resp.errors is None
    assert respdata["id"] == row["id"]
    memberids = list(map(lambda item: item['user']['id'], respdata["memberships"]))

    # vlozit vsechny uzivatele, kteri nejsou cleny
    table2 = data['users']
    for row2 in table2:
        if row2['id'] in memberids:
            continue

        query = """query($id: ID!, $userId: ID!) {
            groupById(id: $id) {
                editor{
                    id
                    addMembership(userId: $userId) {
                        id
                    }
                }
                id
            }
            }"""

        context_value = await createContext(async_session_maker)
        variable_values = {"id": row["id"], "userId": row2["id"]}
        resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

        assert resp.errors is None


    query = """query($id: ID!) {
        groupById(id: $id) {
            memberships {
                user { id }
            }
            id
        }
        }"""

    context_value = await createContext(async_session_maker)
    variable_values = {"id": row["id"]}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
    assert resp.errors is None
    respdata = resp.data["groupById"]
    assert respdata["id"] == row["id"]

    memberids = list(map(lambda item: item['user']['id'], respdata["memberships"]))
    # overit, ze vsichni uzivatele jsou cleny
    table2 = data['users']
    for row2 in table2:
        if row2['id'] in memberids:
            continue
        assert False

import datetime

@pytest.mark.asyncio
async def test_query_group_editor_update():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['groups']
    row = table[0]

    query = """query($id: ID!) {
        groupById(id: $id) {
            id
            lastchange
        }
        }"""

    context_value = await createContext(async_session_maker)
    variable_values = {"id": row["id"]}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

    assert resp.errors is None
    respdata = resp.data["groupById"]
    lastchange = respdata["lastchange"]
    print(lastchange)
    lastchange = datetime.datetime.fromisoformat(respdata["lastchange"])
    print(lastchange)
    query = """query($id: ID!, $group: GroupUpdateGQLModel!) {
        groupById(id: $id) {
            editor{
                id
                update(group: $group) {
                    result
                }
            }
            id
        }
        }"""

    # musi selhat, je spatne razitko
    group = {"name": "newname", "lastchange": f"{datetime.datetime.now().isoformat()}"}
    print(1, group, flush=True)
    context_value = await createContext(async_session_maker)
    variable_values = {"id": row["id"], "group": group}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

    assert resp.errors is None
    respdata = resp.data["groupById"]
    assert respdata["id"] == row["id"]
    assert respdata["editor"]["id"] == row["id"]
    respdata = respdata["editor"]
    assert respdata["update"]["result"] == "fail"

    # musi projit, je spravne razitko
    group = {"name": "newname", "lastchange": f"{lastchange.isoformat()}"}
    print(2, group, flush=True)
    context_value = await createContext(async_session_maker)
    variable_values = {"id": row["id"], "group": group}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

    assert resp.errors is None
    respdata = resp.data["groupById"]
    assert respdata["id"] == row["id"]
    assert respdata["editor"]["id"] == row["id"]
    respdata = respdata["editor"]
    assert respdata["update"]["result"] == "ok"

@pytest.mark.asyncio
async def test_query_group_editor_create_user():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['groups']
    row = table[0]
    query = """query($id: ID!, $user: UserInsertGQLModel!) {
        groupById(id: $id) {
            editor{
                id
                createUser(user: $user) {
                    id
                    name
                    surname
                    email
                    valid
                    lastchange
                }
            }
            id
        }
        }"""

    newuser = {"name": "new", "surname": "user", "email": "new.user@somewhere.else", "valid": True}

    context_value = await createContext(async_session_maker)
    variable_values = {"id": row["id"], "user": newuser}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

    respdata = resp.data["groupById"]

    assert resp.errors is None
    assert respdata["id"] == row["id"]

    respuser = respdata["editor"]["createUser"]
    assert respuser["name"] == newuser["name"]
    assert respuser["surname"] == newuser["surname"]
    assert respuser["email"] == newuser["email"]
    assert respuser["valid"] == newuser["valid"]


@pytest.mark.asyncio
async def test_query_group_editor_add_role():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['groups']
    row = table[0]
    query = """query($id: ID!, $userId: ID!, $roletypeId: ID!) {
        groupById(id: $id) {
            editor{
                id
                addRole(userId: $userId, roletypeId: $roletypeId) {
                    id
                }
            }
            id
        }
        }"""

    roletype = data['roletypes'][0]
    user = data['users'][0]
    context_value = await createContext(async_session_maker)
    variable_values = {"id": row["id"], "userId": user['id'], "roletypeId": roletype['id']}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

    respdata = resp.data["groupById"]

    assert resp.errors is None
    assert respdata["id"] == row["id"]

    resprole = respdata["editor"]["addRole"]


@pytest.mark.asyncio
async def test_query_group_editor_add_role():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['roles']
    row = table[0]
    query = """query($id: ID!, $roleId: ID!) {
        groupById(id: $id) {
            editor{
                id
                invalidateRole(roleId: $roleId) {
                    id
                    valid
                }
            }
            id
        }
        }"""

    context_value = await createContext(async_session_maker)
    variable_values = {"id": row["group_id"], "roleId": row['id']}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

    respdata = resp.data["groupById"]

    assert resp.errors is None
    assert respdata["id"] == row["group_id"]

    resprole = respdata["editor"]["invalidateRole"]
    assert resprole["valid"] == False

@pytest.mark.asyncio
async def test_query_random_university():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    name = "U of IT"
    query = """query($name: String!) {
        randomUniversity(name: $name) {
            id
            name
        }
        }"""

    context_value = await createContext(async_session_maker)
    variable_values = {"name": name}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

    respdata = resp.data["randomUniversity"]

    assert resp.errors is None
    assert respdata["name"] == name

@pytest.mark.asyncio
async def test_query_group_3L():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    letters = "Uni"
    query = """query($letters: String!) {
        groupByLetters(letters: $letters) {
            id
            name
        }
        }"""

    context_value = await createContext(async_session_maker)
    variable_values = {"letters": letters}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

    respdata = resp.data["groupByLetters"]
    for group in respdata:
        assert letters in group['name']

    assert resp.errors is None

@pytest.mark.asyncio
async def test_query_user_3L():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data['users']
    letters = table[0]['name']
    query = """query($letters: String!) {
        userByLetters(letters: $letters) {
            id
            name
        }
        }"""

    context_value = await createContext(async_session_maker)
    variable_values = {"letters": letters}
    resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)

    respdata = resp.data["userByLetters"]
    for user in respdata:
        assert letters in user['name']

    assert resp.errors is None
