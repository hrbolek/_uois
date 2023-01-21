from doctest import master
from functools import cache
import json
import random 
import uuid
from datetime import date, timedelta
import asyncio

from gql_publication.DBDefinitions import BaseModel, UserModel, PublicationModel, AuthorModel, PublicationTypeModel


import itertools

from functools import cache


# fileName = 'gql_publication/publications_dataset.json'

# async def loadDataFromFIle():
#     import aiofiles
#     try:
#         async with aiofiles.open(fileName, mode='r') as publicationsFile:
#             file =  await publicationsFile.read()
            
#     except OSError:
#         print(f'Could not read file: {fileName}')
#     parsedFile =  json.loads(file)
#     return  parsedFile 


# class UUIDEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, UUID):
#             # if the obj is uuid, we simply return the value of uuid
#             return obj.hex
#         return json.JSONEncoder.default(self, obj)

limit = 5

def randomUUID():
    uuids = [uuid.uuid4() for _ in range(limit) ]
    return uuids

userIDs = randomUUID()
authorIDs = randomUUID()
publicationIDs = randomUUID()
publicationTypesIds = randomUUID()


def randomAuthor(id):
    return  {
        'id': id,
        'user_id': random.choice(userIDs),
        'publication_id': random.choice(publicationIDs),
        'order': randomOrder(),
        'share': randomShare()
        }
      

def randomPublicationName():
    publicationNames = [
        "Database systems", "Data Mining", "Algorithms and Data Structures", "Web Data Mining",
        "Zaklady siti", "Telekomunikacni technika"
    ]
    return random.choice(publicationNames)

def randomReference():

    return 'Monografie: FINKE, Manfred. Sulzbach im 17. Jahrhundert : zur Kulturgeschichte einer süddeutschen Residenz. Regensburg : Friedrich Pustet, 1998. 404 s. ISBN 3-7917-1596-8.'

def randomPlace():
    places = ["Brno", "Praha", "Ostrava","Plzen", "Olomouc"]
    return random.choice(places)
    

def randomPublishedDate():
    defualt_date = date(2015, 6, 3)
    return defualt_date + timedelta(days=random.randint(1,100))

def randomShare():
    return int(100/(random.randint(1,4)))

def randomOrder():
    return random.randint(1,2)

def randomPublicationTypes():
   names = ["Skripta", "Clanek v odbornem periodiku", "Konferencni prispevek", "Clanek", "Recenze"]
    
   return [{"id": id, "name": name} for id, name in zip(publicationTypesIds,names)]


def randomPublications(id):
    return {
            "id": id, "name": randomPublicationName(), "publication_type_id": random.choice(publicationTypesIds), "place": randomPlace(), "published_date": randomPublishedDate(),"reference": randomReference(), "valid": True}


from sqlalchemy.future import select


def createDataStructurePublications():
    publications = [randomPublications(id) for id in publicationIDs]
    return publications


def createDataStructureAuthors():
    authors = [randomAuthor(id) for id in authorIDs]
    return authors

def createDataStructureUsers():
    users = [{"id":id }for id in userIDs]
    return users



def createDataStructurePublicationTypes():
    publicationsTypes = randomPublicationTypes()
    return publicationsTypes



# with open('publications_dataset.json', 'w') as outfile:
#     json.dump(dataset, outfile,cls=UUIDEncoder)

from sqlalchemy.future import select

async def randomDataStructure(session):

    publication_types = createDataStructurePublicationTypes()
    publicationsTypesToAdd = [PublicationTypeModel(**record) for record in publication_types]
    
    async with session.begin():
        session.add_all(publicationsTypesToAdd)
    await session.commit()
    
    publications = createDataStructurePublications()
    publicationsToAdd = [PublicationModel(**record) for record in publications]
    async with session.begin():
        session.add_all(publicationsToAdd)
    await session.commit()


    users = createDataStructureUsers()
    usersToAdd = [UserModel(**record) for record in users]
    async with session.begin():
        session.add_all(usersToAdd)
    await session.commit()
    
    authors =  createDataStructureAuthors()
    authorsToAdd = [AuthorModel(**record) for record in authors]
    async with session.begin():
        session.add_all(authorsToAdd)
    await session.commit()

    return publicationsToAdd[0]

    



