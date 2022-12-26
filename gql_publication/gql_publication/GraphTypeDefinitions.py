from typing import List, Union, Optional
import typing
from unittest import result
import strawberry as strawberryA
import uuid

import datetime


from gql_publication.GraphResolvers import resolvePublicationById,resolvePublicationAll, resolveAuthorById, resolvePublicationTypeAll, resolvePublicationTypeById, resolvePublicationForPublicationType, resolveUpdatePublication, resolveAuthorsForPublication, resolvePublicationsForSubject, resolveAuthorByUser


# from gql_publication.GraphResolvers import resolvePublicationById

def AsyncSessionFromInfo(info):
    return info.context['session']




@strawberryA.federation.type(extend=True, keys=["id"],description="""Entity representing a subject""")
class PlanSubjectGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)
    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return PlanSubjectGQLModel(id=id)


@strawberryA.federation.type(extend=True, keys=["id"],description="""Entity representing a realition between Publication and Subject""")
class SubjectGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)
    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return SubjectGQLModel(id=id)

    @strawberryA.field(description="""List of publications with this type""")
    async def publications(self, info: strawberryA.types.Info) -> typing.List['PublicationGQLModel']:
        result = await resolvePublicationsForSubject(AsyncSessionFromInfo(info), self.id)
        return result




@strawberryA.federation.type(extend=True, keys=["id"],description="""Entity representing a user""")
class UserGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""List of authors""")
    async def author_publications(self, info: strawberryA.types.Info) -> typing.List['AuthorGQLModel']:
        result = await resolveAuthorByUser(AsyncSessionFromInfo(info),self.id)
        
      


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
    
    @strawberryA.field(description="""If a publication is valid""")
    def valid(self) -> bool:
        return self.valid

    @strawberryA.field(description="""List of authors, where the author participated in publication""")
    async def authors(self, info: strawberryA.types.Info) -> typing.List['AuthorGQLModel']:
        result = await resolveAuthorsForPublication(AsyncSessionFromInfo(info), self.id)
        return result
   
    @strawberryA.field(description="""Publication type""")
    async def publicationtype(self, info: strawberryA.types.Info) -> PublicationTypeGQLModel:
        result = await resolvePublicationTypeById(AsyncSessionFromInfo(info), self.publication_type_id)
        return result
    
    @strawberryA.field(description="""returns the publication editor if possible""")
    async def editor(self, info: strawberryA.types.Info) -> Union['PublicationEditorGQLModel', None]:
        ## current user must be checked if has rights to get the editor
        ## if not, then None value must be returned
        return self
    

@strawberryA.input
class PublicationUpdateGQLModel:
    name:  Optional[str] = None
    place: Optional[str] = None
    published_date: Optional[datetime.date] = None 
    reference: Optional[str] = None
    publication_type_id: Optional[uuid.UUID] = None
    valid: Optional[bool] = None



@strawberryA.input
class PublicationInsertGQLModel:
    id: Optional[uuid.UUID] = None
    name:  Optional[str] = None
    place: Optional[str] = None
    published_date: Optional[datetime.date] = None 
    reference: Optional[str] = None
    publication_type_id: Optional[uuid.UUID] = None
    valid: Optional[bool] = None


from gql_publication.GraphResolvers import resolveUpdateAuthor, resolveInsertAuthor, resolveUpdateAuthorOrder

@strawberryA.federation.type(keys=["id"], description="""Entity representing an editable publication""")
class PublicationEditorGQLModel:

    ##
    ## Mutace, obejiti problemu s federativnim API
    ##

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolvePublicationById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Updates publication data""")
    async def update(self, info: strawberryA.types.Info, data: PublicationUpdateGQLModel) -> 'PublicationGQLModel':
        result = await resolveUpdatePublication(AsyncSessionFromInfo(info), id=self.id, data=data)
        return result

    @strawberryA.field(description="""Sets author a share""")
    async def set_author_share(self, info: strawberryA.types.Info, author_id: uuid.UUID, share: float) -> 'AuthorGQLModel':
        result = await resolveUpdateAuthor(AsyncSessionFromInfo(info),author_id, data=None, extraAttributes={'share': share})
        return result
    
    @strawberryA.field(description="""Updates the author data""")
    async def set_author_order(self, info: strawberryA.types.Info, author_id: uuid.UUID, order) -> List['AuthorGQLModel']:
        result = await resolveUpdateAuthorOrder(AsyncSessionFromInfo(info),self.id, author_id, order)
        return result


    @strawberryA.field(description="""Create a new author""")
    async def add_author(self, info: strawberryA.types.Info, user_id: uuid.UUID) -> 'AuthorGQLModel':
        result = await resolveInsertAuthor(AsyncSessionFromInfo(info), None, 
            extraAttributes={'user_id': user_id, 'publication_id': self.id})
        return result
        
#######################
    
    @strawberryA.field(description="""Invalidate a publication""")
    async def invalidate_publication(self, info: strawberryA.types.Info) -> PublicationGQLModel:
        session = AsyncSessionFromInfo(info)
        publication = await resolvePublicationById(session, self.id)
        publication.valid = False
        await session.commit()
        return publication




@strawberryA.federation.type(keys=["id"], description="""Entity representing a relation between an user and a publication""")
class AuthorGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveAuthorById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result
  
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
        return self.publication
   
    @strawberryA.field(description="""If an author is valid""")
    def valid(self) -> bool:
        return self.valid




from gql_publication.DBFeeder import randomDataStructure

@strawberryA.type(description="""Type for query root""")
class Query:

    @strawberryA.field(description="""Returns a list of publications (paged)""")
    async def publication_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[PublicationGQLModel]:
        result = await resolvePublicationAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds a publication by their id""")
    async def publication_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[PublicationGQLModel, None]:
        result = await resolvePublicationById (AsyncSessionFromInfo(info), id)
        return result


    @strawberryA.field(description="""Finds an author by their id""")
    async def author_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[AuthorGQLModel, None]:
        result = await resolveAuthorById (AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Finds a publication by their id""")
    async def publication_type_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[PublicationTypeGQLModel]:
        result = await resolvePublicationTypeAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds a group type by its id""")
    async def publication_type_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[PublicationTypeGQLModel, None]:
        result = await resolvePublicationTypeById(AsyncSessionFromInfo(info), id)
        return result


    @strawberryA.field(description="""Random publications""")
    async def randomPublication(self, info: strawberryA.types.Info) -> List[PublicationGQLModel]:
        result = await randomDataStructure(AsyncSessionFromInfo(info))
        # print('random university id', newId)
        # result = await resolveGroupById(AsyncSessionFromInfo(info), newId)
        # print('db response', result.name)
        return result

Schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,))