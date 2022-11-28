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
#
# priklad rozsireni UserGQLModel
#
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id) # jestlize rozsirujete, musi byt tento vyraz

#     zde je rozsireni o dalsi resolvery
#     @strawberryA.field(description="""Inner id""")
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(AsyncSessionFromInfo(info), self.id)
#         return result



from gql_publications.GraphResolvers import resolvePublicationById,resolvePublicaitonAll, resolveAuthorById, resolvePublicationTypeAll, resolvePublicationTypeById, resolvePublicationForPublicationType, resolveUpdatePublication, resolveAuthorForPublication, resolveUserForAuthor


@strawberryA.federation.type(keys=["id"], description="""Entity representing a publication type""")
class PublicationTypeGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolvePublicationTypeById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result
    
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""type""")
    def type(self) -> str:
        return self.type

    @strawberryA.field(description="""List of publications with this type""")
    async def publications(self, info: strawberryA.types.Info) -> typing.List['PublicationGQLModel']:
        result = await resolvePublicationForPublicationType(AsyncSessionFromInfo(info), self.id)
        return result

import datetime

@strawberryA.federation.type(keys=["id"],description="""Entity representing a publication""")
class PublicationGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolvePublicationById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result
    
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""published year""")
    def published_date(self) -> datetime.date:
        return self.published_date

    @strawberryA.field(description="""place""")
    def place(self) -> str:
        return self.place

    @strawberryA.field(description="""reference""")
    def reference(self) -> str:
        return self.reference

    @strawberryA.field(description="""List of authors, where the author participated in publication""")
    async def author(self, info: strawberryA.types.Info) -> typing.List['AuthorGQLModel']:
        result = await resolveAuthorForPublication(AsyncSessionFromInfo(info), self.id)
        return result
   
    @strawberryA.field(description="""Publication type""")
    async def publicationtype(self, info: strawberryA.types.Info) -> PublicationTypeGQLModel:
        result = await resolvePublicationTypeById(AsyncSessionFromInfo(info), self.publication_type_id)
        return result
    


@strawberryA.input
class PublicationUpdateGQLModel:
    name: str = None
    place: str = None
    published_date: datetime.date = None 
    reference:str = None
    publication_type_id: uuid.UUID = None
    valid:bool = None


@strawberryA.federation.type(keys=["id"], description="""Entity representing an editable publication""")
class PublicationEditorGQLModel:

    ##
    ## Mutace, obejiti problemu s federativnim API
    ##
    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Updates the publication data""")
    async def update(self, info: strawberryA.types.Info, data: PublicationUpdateGQLModel) -> PublicationGQLModel:
        result = await resolveUpdatePublication(AsyncSessionFromInfo(info), id=self.id, data=data)
        return result




@strawberryA.federation.type(keys=["id"], description="""Entity representing a relation between an user and a publication""")
class AuthorGQLModel:

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""""")
    def share(self) -> float:
        return self.share
    
    @strawberryA.field(description="""user""")
    async def user(self) -> 'UserGQLModel':
        return self.user

    @strawberryA.field(description="""publication""")
    async def publication(self) -> 'PublicationGQLModel':
        return self.user
   
###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################


@strawberryA.type(description="""Type for query root""")
class Query:

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello_publications(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result

    @strawberryA.field(description="""Returns a list of publications (paged)""")
    async def publication_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[PublicationGQLModel]:
        result = await resolvePublicaitonAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds a publication by their id""")
    async def publication_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[PublicationGQLModel, None]:
        result = await resolvePublicationById(AsyncSessionFromInfo(info), id)
        return result


    @strawberryA.field(description="""Finds an author by their id""")
    async def author_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[AuthorGQLModel, None]:
        result = await resolveAuthorById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Finds a publication by their id""")
    async def publication_type_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[PublicationTypeGQLModel]:
        result = await resolvePublicationTypeAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds a group type by its id""")
    async def publication_type_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[PublicationTypeGQLModel, None]:
        result = await resolvePublicationTypeById(AsyncSessionFromInfo(info), id)
        return result


###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))