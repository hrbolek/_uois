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
from gql_empty.GraphResolvers import resolveRequestById, resolveRequestAll, resolveSectionsForRequest

#define the type help to get attribute name and name 
@strawberryA.federation.type(keys = ["id"] ,description="""Request""")
class RequestGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        #how to fetch request from database
        result = await resolveRequestById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result
    @strawberryA.field(description="""id""")
    async def id(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.id
        #resovle will be ask 
        return result
    #for the name attribute
    @strawberryA.field(description="""name""")
    async def name(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.name
        #resovle will be ask 
        return result
    @strawberryA.field(description="""List of sections in the request""")
    async def sections(self, info: strawberryA.types.Info) -> typing.List['SectionGQLModel']:
        result = await resolveSectionsForRequest(AsyncSessionFromInfo(info), self.id)
        return result

from gql_empty.GraphResolvers import resolveSectionById, resolvePartsForSection

#define the type help to get attribute name and name 
@strawberryA.federation.type(keys = ["id"] ,description="""Section""")
class SectionGQLModel:
    @classmethod 
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveSectionById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result
    @strawberryA.field(description="""id""")
    async def id(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.id
        return result
    @strawberryA.field(description="""name""")
    async def name(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.name
        return result
    @strawberryA.field(description="""List of sections in the request""")
    async def parts(self, info: strawberryA.types.Info) -> typing.List['PartGQLModel']:
        result = await resolvePartsForSection(AsyncSessionFromInfo(info), self.id)
        return result

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def requests(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[RequestGQLModel, None]:
        result = await resolveRequestAll(AsyncSessionFromInfo(info) ,id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def request_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[RequestGQLModel, None]:
        result = await resolveRequestById(AsyncSessionFromInfo(info) ,id)
        #u r getting the database sections , u srxtracting calling the function, returning the data from the table, able to extract , ask for it by Id there will be call the record 
        return result




# from gql_ug.GraphResolvers import resolveUserById, resolveUserAll, resolveUserByRoleTypeAndGroup
# from gql_ug.GraphResolvers import resolveGroupById, resolveGroupTypeById, resolveGroupAll, resolveGroupTypeAll
# from gql_ug.GraphResolvers import resolveAllRoleTypes
# from gql_ug.GraphResolvers import resolveUsersByThreeLetters, resolveGroupsByThreeLetters



#resolver retry partical item from the database, resolverbyID and Alll
#nedd structure 


# check the database if it have the table, u can retry this 
# go to rebulid the decompose, insert arrow in request table, retrieve arrow with the help of , line 52, available from , receive as the response the row, extension 
