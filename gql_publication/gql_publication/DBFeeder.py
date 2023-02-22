
import random 
import uuid
from datetime import date, timedelta

from gql_publication.DBDefinitions import BaseModel, UserModel, PublicationModel, AuthorModel, PublicationTypeModel

limit = 5




def randomUUID():
    """ Generates a random list rondom UUID values 

        Parameters
        ----------
        Returns
        -------
        list
            a list of UUID used for primary keys
"""
    uuids = [uuid.uuid4() for _ in range(limit) ]
    return uuids


""" Initializes lists of UUID for respective models 
"""

userIDs = randomUUID()
authorIDs = randomUUID()
publicationIDs = randomUUID()
publicationTypesIds = randomUUID()


def randomAuthor(id):
    """ Generates a random instance of Author model

        Parameters
        ----------
        id : uuid
            primary key

        Returns
        -------
        object
            an object of author instance
    """  
    return  {
        'id': id,
        'user_id': random.choice(userIDs),
        'publication_id': random.choice(publicationIDs),
        'order': randomOrder(),
        'share': randomShare()
        }
      

def randomPublicationName():
    """ Randomly selects one of predefined publication name values

        Parameters
        ----------

        Returns
        -------
        string
           a string representing name of publication
    """ 

    publicationNames = [
        "Database systems", "Data Mining", "Algorithms and Data Structures", "Web Data Mining",
        "Zaklady siti", "Telekomunikacni technika"
    ]
    return random.choice(publicationNames)

def randomReference():
    """ Randomly selects one of predefined reference values

        Parameters
        ----------

        Returns
        -------
        string
           a string representing name of publication
    """ 
    return 'Monografie: FINKE, Manfred. Sulzbach im 17. Jahrhundert : zur Kulturgeschichte einer süddeutschen Residenz. Regensburg : Friedrich Pustet, 1998. 404 s. ISBN 3-7917-1596-8.'

def randomPlace():
    """ Randomly selects one of predefined place values

        Parameters
        ----------

        Returns
        -------
        string
           a string representing publication place 
    """ 
    places = ["Brno", "Praha", "Ostrava","Plzen", "Olomouc"]
    return random.choice(places)
    

def randomPublishedDate():
    """ Randomly generates a date in the set interval

        Parameters
        ----------

        Returns
        -------
        date
           a date representing date of release
    """ 

    defualt_date = date(2015, 6, 3)
    return defualt_date + timedelta(days=random.randint(1,100))

def randomShare():
    """ Randomly generates an int in the set interval

        Parameters
        ----------

        Returns
        -------
        int
           an int representing author share
    """ 
    return int(100/(random.randint(1,4)))

def randomOrder():
    """ Randomly generates an order of author contribution

        Parameters
        ----------

        Returns
        -------
        int
           an int representing author order
    """ 
    return random.randint(1,2)

def randomPublicationTypes():
    """ Randomly selects one of predefined publication types

        Parameters
        ----------

        Returns
        -------
        string
           a string representing publication type 
    """ 
    names = ["Skripta", "Clanek v odbornem periodiku", "Konferencni prispevek", "Clanek", "Recenze"]
    
    return [{"id": id, "name": name} for id, name in zip(publicationTypesIds,names)]


def randomPublications(id):
    """ Generates a random instance of Publication model

        Parameters
        ----------
         id : uuid
            primary key

        Returns
        -------
        object
           an object of author instance
    """ 
    return {
            "id": id, "name": randomPublicationName(), "publication_type_id": random.choice(publicationTypesIds), "place": randomPlace(), "published_date": randomPublishedDate(),"reference": randomReference(), "valid": True}


from sqlalchemy.future import select


def createDataStructurePublications():
    """ Generates a list of random Publication model instanes

        Parameters
        ----------

        Returns
        -------
        list
           an list of publication instances
    """ 
    publications = [randomPublications(id) for id in publicationIDs]
    return publications


def createDataStructureAuthors():
    """ Generates a list of random Author model instances

        Parameters
        ----------

        Returns
        -------
        list
           an list of author instances
    """ 
    authors = [randomAuthor(id) for id in authorIDs]
    return authors

def createDataStructureUsers():
    """ Generates a list of random User model instances

        Parameters
        ----------

        Returns
        -------
        list
           an list of user instances
    """ 
    users = [{"id":id }for id in userIDs]
    return users


def createDataStructurePublicationTypes():
    """ Generates a list of random PublicationType model instances

        Parameters
        ----------

        Returns
        -------
        list
           an list of publicationtype instances
    """ 
    publicationsTypes = randomPublicationTypes()
    return publicationsTypes


from sqlalchemy.future import select

async def randomDataStructure(session):
    """ Generates a list of random PublicationType model instances

        Parameters
        ----------
        session: session object
        Returns
        -------
        object
           a publication instance
    """ 

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

    



