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



@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result
