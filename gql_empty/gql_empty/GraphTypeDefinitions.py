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
from gql_empty.GraphResolvers import resolveRequestById
from gql_empty.GraphResolvers import resolveRequestAll

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
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def id(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.id
        #resovle will be ask 
        return result

    #for the name attribute
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def name(self, info: strawberryA.types.Info) -> Union[str, None]:
        result = self.name
        #resovle will be ask 
        return result
     # Add more fields here using the @strawberryA.field decorator
     # and using resolvers from GraphResolvers.py to retrieve the data
    
    # id: strawberryA.ID = strawberryA.federation.field(external=True)
    # name: str = strawberryA.Field(description="The name of the request")
    # valid: bool = strawberryA.Field(description="Indicates whether the request is valid or not")

    # @classmethod
    # def resolve_reference(cls, id: strawberryA.ID):
    #     return RequestGQLModel(id=id)
    
    # @strawberryA.field(description="Retrieves the sections related to this request")
    # async def sections(self, info: strawberryA.types.Info) -> List[SectionGQLModel]:
    #     session = AsyncSessionFromInfo(info)
    #     sections = await resolveSectionsForRequest(session, self.id)
    #     return sections
    
    # @strawberryA.field(description="Updates the name and valid status of the request")
    # async def update(self, info: strawberryA.types.Info, name: Optional[str] = None, valid: Optional[bool] = None) -> RequestGQLModel:
    #     session = AsyncSessionFromInfo(info)
    #     update_data = {}
    #     if name is not None:
    #         update_data["name"] = name
    #     if valid is not None:
    #         update_data["valid"] = valid
    #     updated_request = await resolverUpdateRequest(session, self.id, update_data)
    #     return updated_request
    

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello_forms(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
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

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))