from typing import List, Union, Optional
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


from gql_forms.GraphResolvers import resolveUserById, resolveUserAll, resolveUpdateUser, resolveInsertUser
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Request for a user""")
    async def requests(self, info: strawberryA.types.Info)-> List['RequestGQLModel']:
        result = await resolveRequestByUser(AsyncSessionFromInfo(info), self.id)
        return result

############################################################################################
from gql_forms.GraphResolvers import resolveRequestById, resolveRequestAll, resolveSectionsForRequest, resolveUpdateRequest, resolveInsertRequest 

@strawberryA.federation.type(keys = ["id"] ,description="""Entity representing a request""")
class RequestGQLModel:
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    Add more fields here using the @strawberryA.field decorator and using resolvers from GraphResolvers.py to retrieve the data
    """
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
    async def user(self, info: strawberryA.types.Info) -> 'UserGQLModel': #it expect 1 entity
        user = UserGQLModel(id = self.user_id)
        return user

    @strawberryA.field(description="""Request Editor""")
    def editor(self, info: strawberryA.types.Info) ->'RequestEditorGQLModel':
        return self

@strawberryA.input
class RequestUpdateGQLModel:
    lastchange : Optional[datetime.datetime]= datetime.datetime.now()
    name: Optional[str]= None
    status : Optional[str]=None
   
@strawberryA.input
class RequestInsertGQLModel:
    id: Optional[uuid.UUID]= None
    name: Optional[str]= None
    status : Optional[str]=None

@strawberryA.federation.type(keys=["id"],description="""Entity representing an editable Request""")
class RequestEditorGQLModel:
    id: strawberryA.ID = None
    result: str = None
    lastchange: datetime.datetime= None
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveRequestById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""lastchange of data entity""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Result of update operation""")
    async def request(self, info: strawberryA.types.Info) -> RequestGQLModel:
        async with withInfo(info) as session:
            result = await resolveRequestById(session, self.id)
            return result
    @strawberryA.field
    async def insert(self,info: strawberryA.types.Info, creator_id: strawberryA.ID, data: RequestInsertGQLModel)->'RequestGQLModel':
        async with withInfo(info) as session: 
            result = await resolveInsertRequest(session, data=data)
            return result

    @strawberryA.field(description="""Updates the request""")
    async def update(self, info: strawberryA.types.Info, data: RequestUpdateGQLModel) -> 'RequestEditorGQLModel':
        lastchange = self.lastchange
        async with withInfo(info) as session:
            await resolveUpdateRequest(session, id=self.id, data=data)
            if (lastchange < data.lastchange):
                # updating is success
                resultMsg = "ok"
            else:
                # updating is fail
                resultMsg = "fail"
            result = RequestEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result


##################################################################################
from gql_forms.GraphResolvers import resolveSectionById, resolveSectionAll, resolvePartsForSection, resolveUpdateSection, resolveInsertSection

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
    async def request(self, info: strawberryA.types.Info) -> 'RequestGQLModel':
        session = AsyncSessionFromInfo(info)
        request = await resolveRequestById(session, self.request_id)
        return request

    @strawberryA.field(description="""Section Editor""")
    def editor(self, info: strawberryA.types.Info) ->'SectionEditorGQLModel':
        return self

@strawberryA.input
class SectionUpdateGQLModel:
    lastchange : Optional[datetime.datetime]= datetime.datetime.now()
    name: Optional[str]= None
    order : Optional[int]=None
    status : Optional[str]=None
   
@strawberryA.input
class SectionInsertGQLModel:
    id: Optional[uuid.UUID]= None
    name: Optional[str]= None
    order : Optional[int]=None
    status : Optional[str]=None

@strawberryA.federation.type(keys=["id"],description="""Entity representing an editable Section""")
class SectionEditorGQLModel:
    id: strawberryA.ID = None
    result: str = None
    lastchange: datetime.datetime= None
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveSectionById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""lastchange of data entity""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Result of update operation""")
    async def section(self, info: strawberryA.types.Info) -> SectionGQLModel:
        async with withInfo(info) as session:
            result = await resolveSectionById(session, self.id)
            return result
    @strawberryA.field
    async def insert(self,info: strawberryA.types.Info, request_id: strawberryA.ID, data: SectionInsertGQLModel)->'SectionGQLModel':
        async with withInfo(info) as session: 
            result = await resolveInsertSection(session, data=data)
            return result

    @strawberryA.field(description="""Updates the item""")
    async def update(self, info: strawberryA.types.Info, data: SectionUpdateGQLModel) -> 'SectionEditorGQLModel':
        lastchange = self.lastchange
        async with withInfo(info) as session:
            await resolveUpdateSection(session, id=self.id, data=data)
            if (lastchange < data.lastchange):
                # updating is success
                resultMsg = "ok"
            else:
                # updating is fail
                resultMsg = "fail"
            result = SectionEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result


################################################################################################
from gql_forms.GraphResolvers import resolvePartById, resolveItemsForPart, resolveUpdatePart, resolveInsertPart

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
    async def section(self, info: strawberryA.types.Info) -> 'SectionGQLModel':
        session = AsyncSessionFromInfo(info)
        section = await resolveSectionById(session, self.section_id)
        return section

    @strawberryA.field(description="""Part Editor""")
    def editor(self, info: strawberryA.types.Info) ->'PartEditorGQLModel':
        return self

@strawberryA.input
class PartUpdateGQLModel:
    lastchange : Optional[datetime.datetime]= datetime.datetime.now()
    name: Optional[str]= None
    order : Optional[int]=None
   
@strawberryA.input
class PartInsertGQLModel:
    id: Optional[uuid.UUID]= None
    name: Optional[str]= None
    order : Optional[int]=None

@strawberryA.federation.type(keys=["id"],description="""Entity representing an editable Part""")
class PartEditorGQLModel:
    id: strawberryA.ID = None
    result: str = None
    lastchange: datetime.datetime= None
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolvePartById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""lastchange of data entity""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Result of update operation""")
    async def part(self, info: strawberryA.types.Info) -> PartGQLModel:
        async with withInfo(info) as session:
            result = await resolvePartById(session, self.id)
            return result
    @strawberryA.field
    async def insert(self,info: strawberryA.types.Info, section_id: strawberryA.ID, data: PartInsertGQLModel)->'PartGQLModel':
        async with withInfo(info) as session: 
            result = await resolveInsertPart(session, data=data)
            return result

    @strawberryA.field(description="""Updates the item""")
    async def update(self, info: strawberryA.types.Info, data: PartUpdateGQLModel) -> 'PartEditorGQLModel':
        lastchange = self.lastchange
        async with withInfo(info) as session:
            await resolveUpdatePart(session, id=self.id, data=data)
            if (lastchange < data.lastchange):
                # updating is success
                resultMsg = "ok"
            else:
                # updating is fail
                resultMsg = "fail"
            result = PartEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result


#######################################################################################
from gql_forms.GraphResolvers import resolveItemById, resolveItemAll, resolveUpdateItem, resolveInsertItem

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
    def lastchange(self) ->Union[datetime.datetime, None]:
        return self.lastchange
    
    @strawberryA.field(description="""Item's order""")
    def order(self) -> int:
        return self.order
    
    @strawberryA.field(description="""Item's value""")
    def value(self) -> str:
        return self.value
    
    @strawberryA.field(description="Retrieves the part related to this item")
    async def part(self, info: strawberryA.types.Info) -> 'PartGQLModel':
        session = AsyncSessionFromInfo(info)
        part = await resolvePartById(session, self.part_id)
        return part

    @strawberryA.field(description="""Item's value""")
    def editor(self, info: strawberryA.types.Info) ->'ItemEditorGQLModel':
        return self

@strawberryA.input
class ItemUpdateGQLModel:
    lastchange : Optional[datetime.datetime]= datetime.datetime.now()
    name: Optional[str]= None
    order : Optional[int]=None
    value: Optional[str]= None
@strawberryA.input
class ItemInsertGQLModel:
    id: Optional[uuid.UUID]= None
    name: Optional[str]= None
    order : Optional[int]=None
    value: Optional[str]= None

@strawberryA.federation.type(keys=["id"],description="""Entity representing an editable item""")
class ItemEditorGQLModel:
    id: strawberryA.ID = None
    result: str = None
    lastchange: datetime.datetime= None
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveItemById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Result of update operation""")
    async def item(self, info: strawberryA.types.Info) -> ItemGQLModel:
        async with withInfo(info) as session:
            result = await resolveItemById(session, self.id)
            return result
    @strawberryA.field
    async def insert(self,info: strawberryA.types.Info, part_id: strawberryA.ID, data: ItemInsertGQLModel)->'ItemGQLModel':
        async with withInfo(info) as session: 
            result = await resolveInsertItem(session, data=data)
            return result

    @strawberryA.field(description="""Updates the item""")
    async def update(self, info: strawberryA.types.Info, data: ItemUpdateGQLModel) -> 'ItemEditorGQLModel':
        lastchange = self.lastchange
        async with withInfo(info) as session:
            await resolveUpdateItem(session, id=self.id, data=data)
            if (lastchange < data.lastchange):
                # updating is success
                resultMsg = "ok"
            else:
                # updating is fail
                resultMsg = "fail"
            result = ItemEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result
########################################################################

#         EDITOR BY USING MUTATION TYPE- ONE EDITOR FOR ALL ENTITIES

##########################################################################
@strawberryA.input
class OneEditorRequestUpdateGQLModel:
    id: strawberryA.ID
    name: Optional[str]= None
    status : Optional[str]=None

@strawberryA.input
class OneEditorSectionUpdateGQLModel:
    id: strawberryA.ID
    name: Optional[str]= None
    order : Optional[int]=None
    status : Optional[str]=None
   
@strawberryA.input
class OneEditorPartUpdateGQLModel:
    id: strawberryA.ID
    name: Optional[str]= None
    order : Optional[int]=None

@strawberryA.input
class OneEditorItemUpdateGQLModel:
    id: strawberryA.ID
    name: Optional[str]= None
    order : Optional[int]=None
    value: Optional[str]= None

@strawberryA.federation.type(keys=["id"],description="""Entity representing an editable item""")
class EditorGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveItemById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.mutation
    async def insert_request(self,info: strawberryA.types.Info, creator_id: strawberryA.ID, data: RequestInsertGQLModel)->'RequestGQLModel':
        async with withInfo(info) as session: 
            result = await resolveInsertRequest(session, data=data)
            return result

    @strawberryA.mutation
    async def update_request(self, info: strawberryA.types.Info, data: OneEditorRequestUpdateGQLModel)-> 'RequestGQLModel':
        async with withInfo(info) as session:
            result = await resolveUpdateRequest(session, id= data.id, data=data)
            return result
    @strawberryA.mutation
    async def insert_section(self,info: strawberryA.types.Info, request_id: strawberryA.ID, data: SectionInsertGQLModel)->'SectionGQLModel':
        async with withInfo(info) as session: 
            result = await resolveInsertSection(session, data=data)
            return result

    @strawberryA.mutation
    async def update_section(self, info: strawberryA.types.Info, data: OneEditorSectionUpdateGQLModel)-> 'SectionGQLModel':
        async with withInfo(info) as session:
            result = await resolveUpdateSection(session, id= data.id, data=data)
            return result
    @strawberryA.mutation
    async def insert_part(self,info: strawberryA.types.Info,section_id: strawberryA.ID, data: PartInsertGQLModel)->'PartGQLModel':
        async with withInfo(info) as session: 
            result = await resolveInsertPart(session, data=data)
            return result

    @strawberryA.mutation
    async def update_part(self, info: strawberryA.types.Info, data: OneEditorPartUpdateGQLModel)-> 'PartGQLModel':
        async with withInfo(info) as session:
            result = await resolveUpdatePart(session, id= data.id, data=data)
            return result
   
    @strawberryA.mutation
    async def insert_item(self,info: strawberryA.types.Info, part_id: strawberryA.ID, data: ItemInsertGQLModel)->'ItemGQLModel':
        async with withInfo(info) as session: 
            result = await resolveInsertItem(session, data=data)
            return result

    @strawberryA.mutation
    async def update_item(self, info: strawberryA.types.Info, data: OneEditorItemUpdateGQLModel)-> 'ItemGQLModel':
        async with withInfo(info) as session:
            result = await resolveUpdateItem(session, id= data.id, data=data)
            return result

    

from gql_forms.DBFeeder import randomData
from gql_forms.GraphResolvers import resolveRequestByUser, resolveRequestsByStatus, resolveRequestsByThreeLetters

@strawberryA.type(description="""Type for query root""")
class Query:

    @strawberryA.field(description="""Finds an request by their id""")
    async def request_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[RequestGQLModel, None]:
        result = await resolveRequestById(AsyncSessionFromInfo(info) ,id)
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
    
    @strawberryA.field(description="Retrieves requests by their status")
    async def requests_by_status(self, info: strawberryA.types.Info, status: str) -> List[RequestGQLModel]:
        async with withInfo(info) as session: 
            result = await resolveRequestsByStatus(session, status= status)
            return result

    @strawberryA.field(description="""Returns all requests created by a user""")
    async def request_by_user(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[RequestGQLModel, None]:
        result = await resolveRequestByUser(AsyncSessionFromInfo(info) ,id)
        return result

    @strawberryA.field(description="Fills the database with demo form")
    async def fill_request(self, info: strawberryA.types.Info) -> str:
        await randomData(info.context['asyncSessionMaker'])
        return 'fill request successfully'

    @strawberryA.field(description="""Finds an section by their id""")
    async def section_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[SectionGQLModel, None]:
        result = await resolveSectionById(AsyncSessionFromInfo(info) ,id)
        return result

    @strawberryA.field(description="""Finds an part by their id""")
    async def part_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[PartGQLModel, None]:
        result = await resolvePartById(AsyncSessionFromInfo(info) ,id)
        return result

    @strawberryA.field(description="""Finds an item by their id""")
    async def item_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[ItemGQLModel, None]:
        result = await resolveItemById(AsyncSessionFromInfo(info) ,id)
        return result

    @strawberryA.field(description="Retrieves all items")
    async def all_items(self, info: strawberryA.types.Info, skip: int, limit: int) -> List[ItemGQLModel]:
        async with withInfo(info) as session:
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

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ), mutation= EditorGQLModel)