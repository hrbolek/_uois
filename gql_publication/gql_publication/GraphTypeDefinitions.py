from typing import List, Union
import typing
from unittest import result
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

    

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
@strawberryA.federation.type(keys=["id"],description="""Entity representing a publication""")
class PublicationGQLModel:

    @strawberryA.field
    def id(self) -> str:
        return self['id']

    @strawberryA.field
    def name(self) -> str:
        return self['name']

    # @strawberryB.field
    # def users(self) -> typing.List['UserGQLModel']:
    #     print(self['users'])
    #     return [UserGQLModel(user['id']) for user in self['users']]


@strawberryA.federation.type(keys=["id"], description="""Entity representing a relation between an user and a publication""")
class AuthorGQLModel:

    pass


@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result

     @strawberryA.field(description="""Returns a list of publications (paged)""")
    async def publication_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[PublicationGQLModel]:
        result = await resolveUserAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds an user by their id""")
    async def user_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[UserGQLModel, None]:
        result = await resolveUserById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Random publications""")
    async def randomPublication(self, name: str, info: strawberryA.types.Info) -> GroupGQLModel:
        newId = await randomDataStructure(AsyncSessionFromInfo(info), name)
        print('random university id', newId)
        result = await resolveGroupById(AsyncSessionFromInfo(info), newId)
        print('db response', result.name)
        return result