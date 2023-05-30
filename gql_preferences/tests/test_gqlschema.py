
import pytest
import logging
from .shared import (
    prepare_in_memory_sqllite, 
    prepare_demodata, get_demodata, 
    createContext)

from gql_preferences.GraphTypeDefinitions import schema

@pytest.mark.asyncio
async def test_tags():
    tableName = ""
    queryEndpoint = "preferenceEntityTags"
    attributeNames = ["modelId", "modelName"]


    attlist = ' '.join(attributeNames)
    query = "query{" f"{queryEndpoint}" "{" + attlist + "}}"

    async_session_maker = await prepare_in_memory_sqllite()

    
    logging.info(f"query for table {tableName}")

    #query = createByIdQuery(queryEndpoint, attributeNames=attributeNames)
    # query = "query($id: ID!){" f"{queryEndpoint}(id: $id)" "{" + attlist + "}}"

    context_value = await createContext(async_session_maker)
    variable_values = {}
    logging.info(f"test_tags \n{queryEndpoint} {variable_values}\n")

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )  # , variable_values={"title": "The Great Gatsby"})
    assert resp.errors is None
    respdata = resp.data[queryEndpoint]
    assert respdata is not None

    # logging.info(f"respdata \n{respdata}")
    print(f"respdata \n{respdata}")
    ids = list(map(lambda item: item["modelId"], respdata))

    assert "e8479a21-b7c4-4140-9562-217de2656d55" in ids
    assert "2d3d9801-0017-4cf2-9272-2df7b59da667" in ids

    names = list(map(lambda item: item["modelName"], respdata))
    assert "UserGQLModel" in names
    assert "GroupGQLModel" in names

    # "e8479a21-b7c4-4140-9562-217de2656d55": UserGQLModel,
    # "2d3d9801-0017-4cf2-9272-2df7b59da667": GroupGQLModel


@pytest.mark.asyncio
async def test_preference_tags():
    tableName = ""
    queryEndpoint = "preferenceTags"
    attributeNames = ["id", "name"]

    attlist = ' '.join(attributeNames)
    query = "query{" f"{queryEndpoint}" "{" + attlist + "}}"

    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)
    
    logging.info(f"query for table {tableName}")

    #query = createByIdQuery(queryEndpoint, attributeNames=attributeNames)
    # query = "query($id: ID!){" f"{queryEndpoint}(id: $id)" "{" + attlist + "}}"

    context_value = await createContext(async_session_maker)
    variable_values = {}
    logging.info(f"test_preference_tags \n{queryEndpoint} {variable_values}\n")

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )  # , variable_values={"title": "The Great Gatsby"})
    assert resp.errors is None
    respdata = resp.data[queryEndpoint]
    assert respdata is not None

    # logging.info(f"respdata \n{respdata}")
    print(f"respdata \n{respdata}")
    ids = list(map(lambda item: item["id"], respdata))
    assert "b8eebb07-91d5-4d13-8adf-64f4b6de7d06" in ids
    assert "89838aab-d06e-445e-982e-d3c55bc7cb90" in ids
    
@pytest.mark.asyncio
async def test_preference_entities():
    tableName = ""
    queryEndpoint = "preferenceEntities"

    query = "query($tags: [ID!]!){" f"{queryEndpoint}(tags: $tags)" "{ id }}"

    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)
    
    context_value = await createContext(async_session_maker)
    variable_values = {"tags": ["7a4c0d3e-2e3a-4ea0-9037-baa38d8400d2"]}
    logging.info(f"test_preference_entities \n{queryEndpoint} {variable_values}\n")
    print(f"test_preference_entities \n{queryEndpoint} {variable_values}\n{query}")
    

    resp = await schema.execute(
        query, context_value=context_value, variable_values=variable_values
    )  # , variable_values={"title": "The Great Gatsby"})
    assert resp.errors is None
    respdata = resp.data[queryEndpoint]
    assert respdata is not None

    # logging.info(f"respdata \n{respdata}")
    print(f"respdata \n{respdata}")
    assert len(respdata) > 0
    #assert False
    
 


# async def test_tags():
#     tableName = ""
#     queryEndpoint = ""
#     attributeNames = []


#     attlist = ' '.join(attributeNames)
#     query = "query($id: ID!){" f"{queryEndpoint}(id: $id)" "{" + attlist + "}}"

#     async_session_maker = await prepare_in_memory_sqllite()
#     await prepare_demodata(async_session_maker)

#     data = get_demodata()
#     assert data.get(tableName, None) is not None
#     datatable = data[tableName]
#     assert len(datatable) > 0
#     for datarow in datatable:
    
#         logging.info(f"query for table {tableName}")
#         logging.info(f"on entity id={datarow['id']}")
#         logging.info(f"should get {datarow}")

#         #query = createByIdQuery(queryEndpoint, attributeNames=attributeNames)
#         # query = "query($id: ID!){" f"{queryEndpoint}(id: $id)" "{" + attlist + "}}"

#         context_value = await createContext(async_session_maker)
#         variable_values = {"id": datarow["id"]}
#         logging.info(f"createByIdTest \n{queryEndpoint} {variable_values}\n")
        
#         resp = await schema.execute(
#             query, context_value=context_value, variable_values=variable_values
#         )  # , variable_values={"title": "The Great Gatsby"})
#         assert resp.errors is None
#         respdata = resp.data[queryEndpoint]
#         assert respdata is not None

#         compare(respdata, datarow, attributeNames)    