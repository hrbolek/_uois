from doctest import master
from functools import cache
import json
#

import asyncio

from gql_publication.DBDefinitions import BaseModel, UserModel, PublicationModel, AuthorModel, PublicationTypeModel


import itertools

from functools import cache


fileName = 'gql_publication/publications_dataset.json'

async def loadDataFromFIle():
    import aiofiles
    try:
        async with aiofiles.open(fileName, mode='r') as publicationsFile:
            file =  await publicationsFile.read()
            
    except OSError:
        print(f'Could not read file: {fileName}')
    parsedFile =  json.loads(file)
    return  parsedFile 
    

from sqlalchemy.future import select

async def createDataStructurePublication(session,parsedDataset):
      
    # publicationDataset = parsedDataset['publications']
    publicationsToAdd = [PublicationModel(**record) for record in parsedDataset]
    async with session.begin():
        session.add_all(publicationsToAdd)
    await session.commit()


# async def createDataStructurePublicationType(asyncSessionMaker):
async def createDataStructurePublicationType(session,parsedDataset):

    # publicationTypeDataset = parsedDataset['publication_types']
    publicationTypesToAdd = [PublicationTypeModel(**record) for record in parsedDataset]
    async with session.begin():
        session.add_all(publicationTypesToAdd)
    await session.commit()
       
# async def createDataStructureAuthor(asyncSessionMaker):
async def createDataStructureAuthor(session,parsedDataset):
    # authorDataset = parsedDataset['authors']
    authorsToAdd = [AuthorModel(**record) for record in parsedDataset]
    async with session.begin():
        session.add_all(authorsToAdd)
    await session.commit()
    
#     selectedUsers = select(UserModel.id)\
#     selectedUsersIDs = []
#     async with asyncSessionMaker() as session:
#         dbSet = await session.execute(selectedUsers)
#         selectedUsersIDs = dbSet.scalars()

parsedDataset = []    

async def dataLoader():
    task = asyncio.create_task(loadDataFromFIle())
    parsedDataset = await task
    return parsedDataset


data = asyncio.run(dataLoader())




