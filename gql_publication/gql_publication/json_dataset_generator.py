import json
import random
import uuid
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

limit = 10

def randomUUID():
    userIDs = [uuid.uuid4() for _ in range(limit) ]
    return userIDs


def randomAuthor(id):
    return  {
        'id': id,
        'user_id': random.choice(authorIDs),
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
    

def randomPublishedYear():
   return random.randint(1990,2020)


def randomShare():
    return int(100/(random.randint(1,4)))

def randomOrder():
    return random.randint(1,2)

def randomPublicationTypes(ids):
   types = ["Skripta", "Clanek v odbornem periodiku", "Konferencni prispevek", "Clanek", "Recenze"]
    
   return [{"id": id, "type": type} for id, type in zip(ids,types)]


def randomPublications(id):
    return {
        "id": id, "name": randomPublicationName(), "publication_type_id": random.choice(publicationTypesIds), "place": randomPlace(), "published_year": randomPublishedYear(),"reference": randomReference()}

from sqlalchemy.future import select


def createDataStructurePublications():
    publications = [randomPublications(id) for id in publicationIDs]
    return publications


def createDataStructureAuthors():
    authors = [randomAuthor(id) for id in authorIDs]
    return authors

def createDataStructurePublicationTypes():
    publicationsTypes = randomPublicationTypes(publicationTypesIds)
    return publicationsTypes

userIDs = randomUUID()
authorIDs = randomUUID()
publicationIDs = randomUUID()
publicationTypesIds = randomUUID()



publication_types = createDataStructurePublicationTypes()
publications = createDataStructurePublications()
authors =  createDataStructureAuthors()


dataset = {
    "publications": publications,
    "authors": authors,
    "publication_types": publication_types
}


with open('publications_dataset.json', 'w') as outfile:
    json.dump(dataset, outfile,cls=UUIDEncoder)