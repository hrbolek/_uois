from typing import List, Union
import typing
import strawberry as strawberryA
import uuid

def AsyncSessionFromInfo(info):
    return info.context['session']

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
from gql_empty.GraphResolvers import resolveRequestById, resolveRequestAll, resolveSectionsForRequest, resolverUpdateRequest, resolveInsertRequest, resolveRequestsByThreeLetters
# from gql_empty.GraphResolvers import resolveRequestsByThreeLetters
from gql_empty.GraphResolvers import resolveSectionById, resolveSectionAll, resolvePartsForSection, resolverUpdateSection, resolveInsertSection
from gql_empty.GraphResolvers import resolvePartById, resolvePartAll, resolveItemsForPart, resolverUpdatePart, resolveInsertPart
from gql_empty.GraphResolvers import resolveItemById, resolveItemAll, resolverUpdateItem, resolveInsertItem
from gql_empty.GraphResolvers import resolveUserById, resolveUserAll, resolverUpdateUser, resolveInsertUser

@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)



#define the type help to get attribute name and name 
@strawberryA.federation.type(keys = ["id"] ,description="""Type for query root""")
class RequestGQLModel:
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
    @strawberryA.field(description="""Finds an request by their id""")
    async def id(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.id
        #resovle will be ask 
        return result

    #for the name attribute
    @strawberryA.field(description="""Finds an request by their name""")
    async def name(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.name
        #resovle will be ask 
        return result
     # Add more fields here using the @strawberryA.field decorator
     # and using resolvers from GraphResolvers.py to retrieve the data
    
    # id: strawberryA.ID = strawberryA.federation.field(external=True)
    # name: str = strawberryA.Field(description="The name of the request")
    # valid: bool = strawberryA.Field(description="Indicates whether the request is valid or not")
    
    # id: strawberryA.ID = strawberryA.federation.field(external=True)
    # name: str = strawberryA.federation.field(description="""Name of the request""")
    # created: str = strawberryA.federation.field(description="""Timestamp of when the request was created""")
    # valid: bool = strawberryA.federation.field(description="""Whether the request is valid""")
    # # these are the relations
    # sections: List[str] = strawberryA.federation.field(description="""List of section ids that belong to the request""")
    # user: str = strawberryA.federation.field(description="""Id of the user that created the request""")

    # @classmethod
    # def resolve_reference(cls, id: strawberryA.ID):
    #     return RequestGQLModel(id=id)
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveRequestById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result
    
    @strawberryA.field(description="Retrieves the sections related to this request")
    async def sections(self, info: strawberryA.types.Info) -> typing.List['SectionGQLModel']:
        session = AsyncSessionFromInfo(info)
        sections = await resolveSectionsForRequest(session, self.id)
        return sections
    
    # @strawberryA.field(description="Updates the name and valid status of the request")

    
@strawberryA.federation.type(keys = ["id"] ,description="""Type representing a section in the workflow""")
class SectionGQLModel:
   
    @strawberryA.field(description="""Finds an section by their id""")
    async def id(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.id
        #resovle will be ask
        return result

    @strawberryA.field(description="""Finds an section by their id""")
    async def name(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.name
        #resovle will be ask
        return result

    # @classmethod
    # def resolve_reference(cls, id: strawberryA.ID):
    #     return SectionGQLModel(id=id)
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveSectionById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result
    
    @strawberryA.field(description="Retrieves the parts related to this section")
    async def parts(self, info: strawberryA.types.Info) -> typing.List['PartGQLModel']:
        session = AsyncSessionFromInfo(info)
        parts = await resolvePartsForSection(session, self.id)
        return parts

@strawberryA.federation.type(keys = ["id"] ,description="""Type representing a part in the workflow""")
class PartGQLModel:
   
    @strawberryA.field(description="""Finds an part by their id""")
    async def id(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.id
        #resovle will be ask
        return result

    @strawberryA.field(description="""Finds an part by their id""")
    async def name(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.name
        #resovle will be ask
        return result

    # @classmethod
    # def resolve_reference(cls, id: strawberryA.ID):
    #     return PartGQLModel(id=id)
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolvePartById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="Retrieves the items related to this part")
    async def items(self, info: strawberryA.types.Info) -> typing.List['ItemGQLModel']:
        session = AsyncSessionFromInfo(info)
        items = await resolveItemsForPart(session, self.id)
        return items

@strawberryA.federation.type(keys = ["id"] ,description="""Type representing an item in the workflow""")
class ItemGQLModel:
   
    @strawberryA.field(description="""Finds an item by their id""")
    async def id(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.id
        #resovle will be ask
        return result

    @strawberryA.field(description="""Finds an item by their name""")
    async def name(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.name
        #resovle will be ask
        return result
    
    # @classmethod
    # def resolve_reference(cls, id: strawberryA.ID):
    #     return ItemGQLModel(id=id)
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveItemById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

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
    async def all_requests(self, info: strawberryA.types.Info) -> List[RequestGQLModel]:
        session = AsyncSessionFromInfo(info)
        requests = await resolveRequestAll(session)
        return requests

    @strawberryA.field(description="Retrieves requests by three letters in their name")
    async def requests_by_letters(self, info: strawberryA.types.Info, letters: str) -> List[RequestGQLModel]:
        session = AsyncSessionFromInfo(info)
        requests = await resolveRequestsByThreeLetters(session, letters=letters)
        return requests



# from gql_ug.GraphResolvers import resolveUserById, resolveUserAll, resolveUserByRoleTypeAndGroup
# from gql_ug.GraphResolvers import resolveGroupById, resolveGroupTypeById, resolveGroupAll, resolveGroupTypeAll
# from gql_ug.GraphResolvers import resolveAllRoleTypes
# from gql_ug.GraphResolvers import resolveUsersByThreeLetters, resolveGroupsByThreeLetters



#resolver retry partical item from the database, resolverbyID and Alll
#nedd structure 


# check the database if it have the table, u can retry this 
# go to rebulid the decompose, insert arrow in request table, retrieve arrow with the help of , line 52, available from , receive as the response the row, extension 

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))