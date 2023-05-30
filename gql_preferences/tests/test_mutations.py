import pytest
import logging
from .shared import (
    prepare_in_memory_sqllite, 
    prepare_demodata, get_demodata, 
    createContext)

from gql_preferences.GraphTypeDefinitions import schema

@pytest.mark.asyncio
async def test_preference_tag_add():
    query = "mutation($name: String!){ result: tagInsert(tag: {name: $name}) { id msg}}"

    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)
    
    context_value = await createContext(async_session_maker)
    variable_values = {"name": "newName"}   

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    respdata = resp.data["result"]
    assert respdata is not None

    # logging.info(f"respdata \n{respdata}")
    print(f"respdata \n{respdata}")
    assert len(respdata) > 0
    
@pytest.mark.asyncio
async def test_preference_tag_remove():
    query = "mutation($name: String!){ result: tagInsert(tag: {name: $name}) { id msg}}"

    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)
    
    context_value = await createContext(async_session_maker)
    variable_values = {"name": "newName"}   

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    respdata = resp.data["result"]
    assert respdata is not None

    # logging.info(f"respdata \n{respdata}")
    print(f"respdata \n{respdata}")
    assert len(respdata) > 0

    query = "mutation($name: String!){ result: tagDelete(tag: {name: $name}) { id msg}}"

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    respdata = resp.data["result"]
    assert respdata is not None
    print(f"respdata \n{respdata}")
    assert respdata["msg"] == "ok"

@pytest.mark.asyncio
async def test_preference_tag_update():
    query = "mutation($name: String!){ result: tagInsert(tag: {name: $name}) { id msg tag { id lastchange name }}}"

    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)
    
    context_value = await createContext(async_session_maker)
    variable_values = {"name": "newName"}   

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    respdata = resp.data["result"]
    assert respdata is not None
    tagData = respdata["tag"]
    # logging.info(f"respdata \n{respdata}")
    print(f"respdata \n{respdata}")
    assert len(respdata) > 0

    query = "mutation($name: String! $id: ID! $lastchange: DateTime!){ result: tagUpdate(tag: {name: $name id: $id lastchange: $lastchange}) { id msg}}"

    variable_values = {**tagData, "name": "name X"}
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    respdata = resp.data["result"]
    assert respdata is not None
    print(f"respdata \n{respdata}")
    assert respdata["msg"] == "ok"

@pytest.mark.asyncio
async def test_preference_tag_add_to_entity():
    query = "mutation($name: String!){ result: tagInsert(tag: {name: $name}) { id msg tag { id lastchange name }}}"

    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)
    
    context_value = await createContext(async_session_maker)
    variable_values = {"name": "newName"}   

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    respdata = resp.data["result"]
    assert respdata is not None
    tagData = respdata["tag"]
    # logging.info(f"respdata \n{respdata}")
    print(f"respdata \n{respdata}")
    assert len(respdata) > 0


    tables = get_demodata()
    table = tables["users"]
    row = table[0]

    query = "mutation($entityId: ID! $entityTypeId: ID! $tagId: ID! ){ result: tagAddToEntity(tagData: {entityId: $entityId tagId: $tagId entityTypeId: $entityTypeId}) { msg}}"

    variable_values = {"tagId": tagData["id"], "entityTypeId": "e8479a21-b7c4-4140-9562-217de2656d55", "entityId": row["id"]}
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    respdata = resp.data["result"]
    assert respdata is not None
    print(f"respdata \n{respdata}")
    assert respdata["msg"] == "ok"

@pytest.mark.asyncio
async def test_preference_tag_remove_from_entity():
    query = "mutation($name: String!){ result: tagInsert(tag: {name: $name}) { id msg tag { id lastchange name }}}"

    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)
    
    context_value = await createContext(async_session_maker)
    variable_values = {"name": "newName"}   

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    respdata = resp.data["result"]
    assert respdata is not None
    tagData = respdata["tag"]
    # logging.info(f"respdata \n{respdata}")
    print(f"respdata \n{respdata}")
    assert len(respdata) > 0
    
    ###########
    # Tag added
    ###########

    tables = get_demodata()
    table = tables["users"]
    row = table[0]

    query = "mutation($entityId: ID! $entityTypeId: ID! $tagId: ID! ){ result: tagAddToEntity(tagData: {entityId: $entityId tagId: $tagId entityTypeId: $entityTypeId}) { msg}}"

    variable_values = {"tagId": tagData["id"], "entityTypeId": "e8479a21-b7c4-4140-9562-217de2656d55", "entityId": row["id"]}
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    respdata = resp.data["result"]
    assert respdata is not None
    print(f"respdata \n{respdata}")
    assert respdata["msg"] == "ok"

    ###########
    # Tag assigned
    ###########

    query = "mutation($entityId: ID! $tagId: ID! ){ result: tagRemoveFromEntity(tagData: {entityId: $entityId tagId: $tagId }) { msg}}"

    variable_values = {"tagId": tagData["id"], "entityId": row["id"]}
    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )
    assert resp.errors is None
    respdata = resp.data["result"]
    assert respdata is not None
    print(f"respdata \n{respdata}")
    assert respdata["msg"] == "ok"

    ###########
    # Tag removed
    ###########