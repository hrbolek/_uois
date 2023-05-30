import sqlalchemy
from sqlalchemy import select
import pytest
import logging

from tests.shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
)

from gql_preferences.GraphTypeDefinitions import schema

def createDBTest(tableName, dbModel):
    
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        table = data[tableName]

        
        for row in table:
            
            async with  async_session_maker() as session:
                rowid = row['id']
                stmt = select(dbModel).filter_by(id=rowid)
                result = await session.execute(stmt)
                row = result.scalar()
                # row = select(dbModel).filter_by(id=rowid).execute(session)
                
            assert row is not None

    return result_test


def compare(rowa, rowb, attributeNames, skipattributes=["lastchange", "created", "createdBy", "changedBy"]):
    for attName in attributeNames:
        if attName in skipattributes: continue
        
        assert rowa[attName] == rowb[attName]
    return

def createByIdQuery(queryEndpoint, attributeNames=["id", "name"]):
    attlist = ' '.join(attributeNames)
    query = "query($id: ID!){" f"{queryEndpoint}(id: $id)" "{" + attlist + "}}"
    return query

def createPageQuery(queryEndpoint, attributeNames=["id", "name"]):
    attlist = ' '.join(attributeNames)
    query = "query{" f"{queryEndpoint}" "{" + attlist + "}}"
    return query

def createReferenceQuery(gqltype, attributeNames):
    attlist = ' '.join(attributeNames)
    query = (
        'query($id: ID!) { _entities(representations: [{ __typename: '+ f'"{gqltype}", id: $id' + 
        ' }])' +
        '{' +
        f'...on {gqltype}' + 
        '{ ' + attlist + '}'+
        '}' + 
        '}')
    return query


def createReferenceQueryStAtts(gqltype):
    query = (
        'query($id: ID!) { _entities(representations: [{ __typename: '+ f'"{gqltype}", id: $id' + 
        ' }])' +
        '{' +
        f'...on {gqltype}' + 
        '{ id createdBy { id } changedBy { id } lastchange created }'+
        '}' + 
        '}')
    return query


def createByIdTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    # attlist = ' '.join(attributeNames)
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        assert data.get(tableName, None) is not None
        datatable = data[tableName]
        assert len(datatable) > 0
        for datarow in datatable:
        
            logging.info(f"query for table {tableName}")
            logging.info(f"on entity id={datarow['id']}")
            logging.info(f"should get {datarow}")

            query = createByIdQuery(queryEndpoint, attributeNames=attributeNames)
            # query = "query($id: ID!){" f"{queryEndpoint}(id: $id)" "{" + attlist + "}}"

            context_value = await createContext(async_session_maker)
            variable_values = {"id": datarow["id"]}
            logging.info(f"createByIdTest \n{queryEndpoint} {variable_values}\n")
            
            resp = await schema.execute(
                query, context_value=context_value, variable_values=variable_values
            )  # , variable_values={"title": "The Great Gatsby"})
            assert resp.errors is None
            respdata = resp.data[queryEndpoint]
            assert respdata is not None

            compare(respdata, datarow, attributeNames)
            # for attName in attributeNames:
            #     if attName == "lastchange": continue
            #     assert respdata[attName] == datarow[attName]

    return result_test

from tests.shared import createGQLClient
def createByIdTestApp(tableName, queryByIdEndpoint, attributeNames=["id", "name"]):
    # attlist = ' '.join(attributeNames)
    @pytest.mark.asyncio
    async def result_test():
        client = createGQLClient()
        data = get_demodata()
        assert data.get(tableName, None) is not None
        datatable = data[tableName]
        assert len(datatable) > 0
        logging.info(f"query for table {tableName}")
        query = createByIdQuery(queryByIdEndpoint, attributeNames=attributeNames)
        for datarow in datatable:
        
            logging.info(f"on entity id={datarow['id']}")
            logging.info(f"should get {datarow}")

            variable_values = {"id": datarow["id"]}

            resp = client.post("/gql", json={"query": query, "variables": variable_values})
            assert resp.status_code == 200
            resp = resp.json()
            logging.info(resp)
            assert resp.get("errors", None) is None
            respdata = resp["data"].get(queryByIdEndpoint, None)
            assert respdata is not None

            compare(respdata, datarow, attributeNames)
            # for attName in attributeNames:
            #     if attName == "lastchange": continue
            #     assert respdata[attName] == datarow[attName]

    return result_test

def createPageTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    # attlist = ' '.join(attributeNames)
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()

        # query = "query{" f"{queryEndpoint}" "{" + attlist + "}}"
        query = createPageQuery(queryEndpoint=queryEndpoint, attributeNames=attributeNames)

        context_value = await createContext(async_session_maker)
        resp = await schema.execute(query, context_value=context_value)
        assert resp.errors is None

        respdata = resp.data[queryEndpoint]
        datarows = data[tableName]


        for rowa, rowb in zip(respdata, datarows):
            compare(rowa, rowb, attributeNames)
            # for attName in attributeNames:
            #     if attName == "lastchange": continue
            #     assert rowa[attName] == rowb[attName]

    return result_test

def createPageTestApp(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        client = createGQLClient()

        query = createPageQuery(queryEndpoint=queryEndpoint, attributeNames=attributeNames)
        variable_values = {}

        resp = client.post("/gql", json={"query": query, "variables": variable_values})
        assert resp.status_code == 200
        resp = resp.json()
        logging.info(resp)
        assert resp.get("errors", None) is None
        respdata = resp["data"].get(queryEndpoint, None)
        assert respdata is not None

        datarows = data[tableName]
        for rowa, rowb in zip(respdata, datarows):
            compare(rowa, rowb, attributeNames)

    return result_test


def createResolveReferenceTest(tableName, gqltype, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        table = data[tableName]
        query = createReferenceQuery(gqltype, attributeNames=attributeNames)
        query2 = createReferenceQueryStAtts(gqltype)
        for row in table:
            rowid = row['id']
           
            variable_values = {"id": rowid}
            context_value = await createContext(async_session_maker)
            resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
            assert resp.errors is None
            data = resp.data
            logging.info(data)
            data = data['_entities'][0]

            compare(data, row, attributeNames)
            
            context_value = await createContext(async_session_maker)
            variable_values = {"id": rowid}
            resp = await schema.execute(query2, context_value=context_value, variable_values=variable_values)
            assert resp.errors is None
            data = resp.data
            logging.info(data)


    return result_test

def createResolveReferenceTestApp(tableName, gqltype, attributeNames=["id", "name"]):
    
    @pytest.mark.asyncio
    async def result_test():

        data = get_demodata()
        table = data[tableName]
        client = createGQLClient()
        query = createReferenceQuery(gqltype, attributeNames=attributeNames)
        query2 = createReferenceQueryStAtts(gqltype)
        for row in table:
            rowid = row['id']      

            variable_values = {"id": rowid}
            resp = client.post("/gql", json={"query": query, "variables": variable_values})
            assert resp.status_code == 200
            resp = resp.json()
            logging.info(resp)
            assert resp.get("errors", None) is None
            data = resp["data"]
            logging.info(data)
            data = data['_entities'][0]

            compare(data, row, attributeNames)
            

            resp = client.post("/gql", json={"query": query2, "variables": variable_values})
            assert resp.status_code == 200
            resp = resp.json()
            logging.info(resp)
            assert resp.get("errors", None) is None
            data = resp["data"]
            logging.info(data)
    return result_test
