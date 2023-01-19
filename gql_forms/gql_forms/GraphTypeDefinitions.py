from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
import datetime

from contextlib import asynccontextmanager

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context['asyncSessionMaker']
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass
def AsyncSessionFromInfo(info):
    return info.context['session']

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
from gql_forms.GraphResolvers import resolveRequestById, resolveRequestAll, resolveSectionsForRequest, resolveUpdateRequest, resolveInsertRequest, resolveRequestsByThreeLetters
# from gql_forms.GraphResolvers import resolveRequestsByThreeLetters
from gql_forms.GraphResolvers import resolveSectionById, resolveSectionAll, resolvePartsForSection, resolveUpdateSection, resolveInsertSection
from gql_forms.GraphResolvers import resolvePartById, resolvePartAll, resolveItemsForPart, resolveUpdatePart, resolveInsertPart
from gql_forms.GraphResolvers import resolveItemById, resolveItemAll, resolveUpdateItem, resolveInsertItem, resolveDeleteItem
from gql_forms.GraphResolvers import resolveUserById, resolveUserAll, resolveUpdateUser, resolveInsertUser


# Editor 
# Change data in database 
# 	1. Have edtior foe changing value 
# 	Some struture for write, how I can compose the data structure to
# Creat one Editor---- GQLModel
# change 

@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        # result = await resolveUserById(AsyncSessionFromInfo(info), id)
        # result._type_definition = cls._type_definition # little hack :)
        return UserGQLModel(id=id)

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    # @strawberryA.field(description="""Request's name (like Vacation)""")
    # def name(self) -> str:
    #     return self.name
    
    # @strawberryA.field(description="""Request's name (like Vacation)""")
    # def email(self) -> str:
    #     return self.name
    
    
    # @strawberryA.field(description="""Request's time of creation""")
    # def create_at(self) -> datetime.datetime:
    #     return self.create_at
    
    # @strawberryA.field(description="""Request's time of last update""")
    # def lastchange(self) -> datetime.datetime:
    #     return self.lastchange
    @strawberryA.field(description="""Request for a user""")
    async def requests(self, info: strawberryA.types.Info)-> List['RequestGQLModel']:
        result = await resolveRequestByUser(AsyncSessionFromInfo(info), self.id)
        return result




#define the type help to get attribute name and name 
@strawberryA.federation.type(keys = ["id"] ,description="""Entity representing a request""")
class RequestGQLModel:
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
     # Add more fields here using the @strawberryA.field decorator
     # and using resolvers from GraphResolvers.py to retrieve the data

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveRequestById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Request's name (like Vacation)""")
    def name(self) -> str:
        return self.name
    
    @strawberryA.field(description="""Request's time of creation""")
    def create_at(self) -> datetime.datetime:
        return self.create_at
    
    @strawberryA.field(description="""Request's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Request's status""")
    def status(self) -> str:
        return self.status
        
    @strawberryA.field(description="Retrieves the sections related to this request")
    async def sections(self, info: strawberryA.types.Info) -> typing.List['SectionGQLModel']:
        session = AsyncSessionFromInfo(info)
        sections = await resolveSectionsForRequest(session, self.id)
        return sections
    
    @strawberryA.field(description="Retrieves the user related to this request")
    async def user(self, info: strawberryA.types.Info) -> typing.List['UserGQLModel']:
        user = UserGQLModel(id = self.user_id)
        return user

    
@strawberryA.federation.type(keys = ["id"] ,description="""Type representing a section in the workflow""")
class SectionGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveSectionById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""Section's name""")
    def name(self) -> str:
        return self.name
    
    @strawberryA.field(description="""Section's time of creation""")
    def create_at(self) -> datetime.datetime:
        return self.create_at
    
    @strawberryA.field(description="""Section's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""Section's order""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""Section's status""")
    def status(self) -> str:
        return self.status
    
    @strawberryA.field(description="Retrieves the parts related to this section")
    async def parts(self, info: strawberryA.types.Info) -> typing.List['PartGQLModel']:
        session = AsyncSessionFromInfo(info)
        parts = await resolvePartsForSection(session, self.id)
        return parts

    @strawberryA.field(description="Retrieves the request related to this section")
    async def request(self, info: strawberryA.types.Info) -> typing.List['RequestGQLModel']:
        session = AsyncSessionFromInfo(info)
        request = await resolveRequestById(session, self.request_id)
        return request


@strawberryA.federation.type(keys = ["id"] ,description="""Type representing a part in the workflow""")
class PartGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolvePartById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result
    
    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""Part's name (part for Student)""")
    def name(self) -> str:
        return self.name
    
    @strawberryA.field(description="""Part's time of creation""")
    def create_at(self) -> datetime.datetime:
        return self.create_at
    
    @strawberryA.field(description="""Part's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""Part's order""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="Retrieves the items related to this part")
    async def items(self, info: strawberryA.types.Info) -> typing.List['ItemGQLModel']:
        session = AsyncSessionFromInfo(info)
        items = await resolveItemsForPart(session, self.id)
        return items
    
    @strawberryA.field(description="Retrieves the section related to this part")
    async def section(self, info: strawberryA.types.Info) -> typing.List['SectionGQLModel']:
        session = AsyncSessionFromInfo(info)
        section = await resolveSectionById(session, self.section_id)
        return section

@strawberryA.federation.type(keys = ["id"] ,description="""Type representing an item in the workflow""")
class ItemGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveItemById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result
    
    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""Item's name (like Name)""")
    def name(self) -> str:
        return self.name
    
    @strawberryA.field(description="""Item's time of creation""")
    def create_at(self) -> datetime.datetime:
        return self.create_at
    
    @strawberryA.field(description="""Item's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""Item's order""")
    def order(self) -> int:
        return self.order
    
    @strawberryA.field(description="""Item's value""")
    def value(self) -> str:
        return self.value
    
    @strawberryA.field(description="Retrieves the part related to this item")
    async def part(self, info: strawberryA.types.Info) -> typing.List['PartGQLModel']:
        session = AsyncSessionFromInfo(info)
        part = await resolvePartById(session, self.part_id)
        return part

from typing import Optional
@strawberryA.input
class ItemUpdateGQLModel:
    name: Optional[str]= None
    #create_at : Optional[datetime.datetime] =None
    order : Optional[int]=None
    value: Optional[str]= None

@strawberryA.input
class ItemInsertGQLModel:
    id: Optional[uuid.UUID]= None
    part_id: Optional[uuid.UUID]= None
    name: Optional[str]= None
    #create_at : Optional[datetime.datetime] =None
    order : Optional[int]=None
    value: Optional[str]= None

@strawberryA.federation.type(keys=["id"],description="""Entity representing an editable item""")
class ItemEditorGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveUserById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field
    async def insert_item(self,info: strawberryA.types.Info,data: ItemInsertGQLModel)->'ItemGQLModel':
        async with withInfo(info) as session:
            result = await resolveInsertItem(session, data=data)
            return result
    @strawberryA.field
    async def update_item(self, info: strawberryA.types.Info, data: ItemUpdateGQLModel, id: strawberryA.ID)-> 'ItemGQLModel':
        async with withInfo(info) as session:
            result = await resolveUpdateItem(session, id=id, data=data)
            return result
    
    #FAIL
    @strawberryA.field
    async def delete_item(self, info: strawberryA.types.Info, id: strawberryA.ID)-> str:
        async with withInfo(info) as session:
            await resolveDeleteItem(session, id=id)
        return "Delete an item"
            


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
from gql_forms.DBFeeder import randomData
from gql_forms.GraphResolvers import resolveRequestByUser

@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Say hello to the world""")
    async def say_hello_forms(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result


    
    @strawberryA.field(description="""Finds an request by their id""")
    async def request_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[RequestGQLModel, None]:
        result = await resolveRequestById(AsyncSessionFromInfo(info) ,id)
        #u r getting the database sections , u srxtracting calling the function, returning the data from the table, able to extract , ask for it by Id there will be call the record 
        return result

    @strawberryA.field(description="Retrieves all requests")
    async def all_requests(self, info: strawberryA.types.Info, skip: int, limit: int) -> List[RequestGQLModel]:
        session = AsyncSessionFromInfo(info)
        requests = await resolveRequestAll(session, skip = skip, limit = limit)
        return requests

    @strawberryA.field(description="Retrieves requests by three letters in their name")
    async def requests_by_letters(self, info: strawberryA.types.Info, letters: str) -> List[RequestGQLModel]:
        session = AsyncSessionFromInfo(info)
        requests = await resolveRequestsByThreeLetters(session, letters=letters)
        return requests


    @strawberryA.field(description="""returns all requests created by a user""")
    async def request_by_user(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[RequestGQLModel, None]:
        result = await resolveRequestByUser(AsyncSessionFromInfo(info) ,id)
        #u r getting the database sections , u srxtracting calling the function, returning the data from the table, able to extract , ask for it by Id there will be call the record 
        return result

    

    @strawberryA.field(description="Fills the database with demo form")
    async def fill_request(self, info: strawberryA.types.Info) -> str:
        await randomData(info.context['asyncSessionMaker'])
        return 'ok'

    @strawberryA.field(description="Retrieves all items")
    async def all_items(self, info: strawberryA.types.Info, skip: int, limit: int) -> List[ItemGQLModel]:
        session = AsyncSessionFromInfo(info)
        items = await resolveItemAll(session, skip = skip, limit = limit)
        return items



###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ), mutation= ItemEditorGQLModel)