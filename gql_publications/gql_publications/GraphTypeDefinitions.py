from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager


@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


def AsyncSessionFromInfo(info):
    print(
        "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]

def getLoaders(info):
    return info.context['all']


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

import datetime

from gql_publications.GraphResolvers import (
    resolvePublicationById,
    resolvePublicationAll,
    resolveAuthorById,
)
from gql_publications.GraphResolvers import (
    resolvePublicationTypeAll,
    resolvePublicationTypeById,
    resolvePublicationForPublicationType,
)
from gql_publications.GraphResolvers import (
    resolveUpdatePublication,
    resolveAuthorsForPublication,
    resolvePublicationsForSubject,
    resolveAuthorsByUser,
)


@strawberryA.federation.type(extend=True, keys=["id"])
class PlanSubjectGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return PlanSubjectGQLModel(id=id)


@strawberryA.federation.type(extend=True, keys=["id"])
class SubjectGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return SubjectGQLModel(id=id)

    @strawberryA.field(description="""List of publications with this type""")
    async def publications(
        self, info: strawberryA.types.Info
    ) -> typing.List["PublicationGQLModel"]:
        async with withInfo(info) as session:
            result = await resolvePublicationsForSubject(session, self.id)
            return result


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""List of authors""")
    async def author_publications(
        self, info: strawberryA.types.Info
    ) -> typing.List["AuthorGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveAuthorsByUser(session, self.id)
            return result


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a publication type"""
)
class PublicationTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolvePublicationTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""type""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""List of publications with this type""")
    async def publications(
        self, info: strawberryA.types.Info
    ) -> typing.List["PublicationGQLModel"]:
        async with withInfo(info) as session:
            result = await resolvePublicationForPublicationType(session, self.id)
            return result


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a publication"""
)
class PublicationGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolvePublicationById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

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

    @strawberryA.field(description="""last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(
        description="""List of authors, where the author participated in publication"""
    )
    async def authors(
        self, info: strawberryA.types.Info
    ) -> typing.List["AuthorGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveAuthorsForPublication(session, self.id)
            return result

    @strawberryA.field(description="""Publication type""")
    async def publicationtype(
        self, info: strawberryA.types.Info
    ) -> PublicationTypeGQLModel:
        async with withInfo(info) as session:
            result = await resolvePublicationTypeById(session, self.publication_type_id)
            return result

    @strawberryA.field(description="""returns the publication editor if possible""")
    async def editor(
        self, info: strawberryA.types.Info
    ) -> Union["PublicationEditorGQLModel", None]:
        ## current user must be checked if has rights to get the editor
        ## if not, then None value must be returned
        return self


from typing import Optional


@strawberryA.input
class _PublicationUpdateGQLModel:
    name: Optional[str] = None
    place: Optional[str] = None
    published_date: Optional[datetime.date] = None
    reference: Optional[str] = None
    publication_type_id: Optional[strawberryA.ID] = None
    valid: Optional[bool] = None


@strawberryA.input
class _PublicationInsertGQLModel:
    id: Optional[strawberryA.ID] = None
    name: Optional[str] = None
    place: Optional[str] = None
    published_date: Optional[datetime.date] = None
    reference: Optional[str] = None
    publication_type_id: Optional[strawberryA.ID] = None
    valid: Optional[bool] = None


from gql_publications.GraphResolvers import (
    resolveUpdateAuthor,
    resolveInsertAuthor,
    resolveUpdateAuthorOrder,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an editable publication"""
)
class PublicationEditorGQLModel:

    ##
    ## Mutace, obejiti problemu s federativnim API
    ##

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolvePublicationById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Updates publication data""")
    async def update(
        self, info: strawberryA.types.Info, data: "PublicationUpdateGQLModel"
    ) -> "PublicationGQLModel":
        async with withInfo(info) as session:
            result = await resolveUpdatePublication(session, id=self.id, data=data)
            return result

    @strawberryA.field(description="""Sets author a share""")
    async def set_author_share(
        self, info: strawberryA.types.Info, author_id: strawberryA.ID, share: float
    ) -> "AuthorGQLModel":
        async with withInfo(info) as session:
            result = await resolveUpdateAuthor(
                session, author_id, data=None, extraAttributes={"share": share}
            )
            return result

    @strawberryA.field(description="""Updates the author data""")
    async def set_author_order(
        self, info: strawberryA.types.Info, author_id: strawberryA.ID, order: int
    ) -> List["AuthorGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveUpdateAuthorOrder(session, self.id, author_id, order)
            return result

    @strawberryA.field(description="""Create a new author""")
    async def add_author(
        self, info: strawberryA.types.Info, user_id: strawberryA.ID
    ) -> "AuthorGQLModel":
        async with withInfo(info) as session:
            result = await resolveInsertAuthor(
                session,
                None,
                extraAttributes={"user_id": user_id, "publication_id": self.id},
            )
            return result

    #######################

    @strawberryA.field(description="""Invalidate a publication""")
    async def invalidate_publication(
        self, info: strawberryA.types.Info
    ) -> PublicationGQLModel:
        async with withInfo(info) as session:
            publication = await resolvePublicationById(session, self.id)
            publication.valid = False
            await session.commit()
            return publication


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a publication""",
)
class AuthorGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveAuthorById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""order in author list""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""share on publication""")
    def share(self) -> float:
        return self.share

    @strawberryA.field(description="""user""")
    async def user(self) -> "UserGQLModel":
        return await UserGQLModel.resolve_reference(self.user_id)

    @strawberryA.field(description="""publication""")
    async def publication(self, info: strawberryA.types.Info) -> "PublicationGQLModel":
        return await PublicationGQLModel.resolve_reference(info, self.publication_id)

    @strawberryA.field(description="""If an author is valid""")
    def valid(self) -> bool:
        return self.valid

    @strawberryA.field(description="""last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################


from gql_publications.DBFeeder import randomDataStructure


@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Returns a list of publications (paged)""")
    async def publication_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[PublicationGQLModel]:
        async with withInfo(info) as session:
            result = await resolvePublicationAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Finds a publication by their id""")
    async def publication_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[PublicationGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolvePublicationById(session, id)
            return result

    @strawberryA.field(description="""Finds an author by their id""")
    async def author_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[AuthorGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveAuthorById(session, id)
            return result

    @strawberryA.field(description="""Gets a list of publication types""")
    async def publication_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[PublicationTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolvePublicationTypeAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Finds a group type by its id""")
    async def publication_type_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[PublicationTypeGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolvePublicationTypeById(session, id)
            return result

    @strawberryA.field(description="""Random publications""")
    async def randomPublication(
        self, info: strawberryA.types.Info
    ) -> List[PublicationGQLModel]:
        async with withInfo(info) as session:
            result = await randomDataStructure(session)
            # print('random university id', newId)
            # result = await resolveGroupById(session,  newId)
            # print('db response', result.name)
            return result


###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

from typing import Optional
import datetime

@strawberryA.input
class PublicationInsertGQLModel:
    name: str
    
    id: Optional[strawberryA.ID] = None
    publication_type_id: Optional[strawberryA.ID] = None
    place: Optional[str] = ""
    published_date: Optional[datetime.datetime] = datetime.datetime.now()
    reference: Optional[str] = ""
    valid: Optional[bool] = True

@strawberryA.input
class PublicationUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID

    name: Optional[str] = None
    publication_type_id: Optional[strawberryA.ID] = None
    place: Optional[str] = None
    published_date: Optional[datetime.datetime] = None
    reference: Optional[str] = None
    valid: Optional[bool] = None
    
    
@strawberryA.type
class PublicationResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of publication operation""")
    async def publication(self, info: strawberryA.types.Info) -> Union[PublicationGQLModel, None]:
        result = await PublicationGQLModel.resolve_reference(info, self.id)
        return result
   

@strawberryA.input
class AuthorInsertGQLModel:
    user_id: strawberryA.ID
    publication_id: strawberryA.ID
    id: Optional[strawberryA.ID] = None
    share: Optional[float] = 0.1
    order: Optional[int] = 1000

@strawberryA.input
class AuthorUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    share: Optional[float] = None
    order: Optional[int] = None
    
@strawberryA.type
class AuthorResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of publication operation""")
    async def author(self, info: strawberryA.types.Info) -> Union[AuthorGQLModel, None]:
        result = await AuthorGQLModel.resolve_reference(info, self.id)
        return result
   
@strawberryA.federation.type(extend=True)
class Mutation:
    @strawberryA.mutation(description="Adds the authorship to the publication, Currently it does not check if the authorship exists.")
    async def author_insert(self, info: strawberryA.types.Info, author: AuthorInsertGQLModel) -> AuthorResultGQLModel:
        loader = getLoaders(info).authors
        row = await loader.insert(author)
        result = AuthorResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="Updates the authorship.")
    async def author_update(self, info: strawberryA.types.Info, author: AuthorUpdateGQLModel) -> AuthorResultGQLModel:
        loader = getLoaders(info).authors
        row = await loader.update(author)
        result = AuthorResultGQLModel()
        result.msg = "ok"
        result.id = author.id
        if row is None:
            result.msg = "fail"
            
        return result

    @strawberryA.mutation(description="Delete the authorship.")
    async def author_delete(self, info: strawberryA.types.Info, authorship_id: strawberryA.ID) -> str:
        loader = getLoaders(info).authors
        await loader.delete(authorship_id)
        return "ok"

    @strawberryA.mutation(description="Create a new publication.")
    async def publication_insert(self, info: strawberryA.types.Info, publication: PublicationInsertGQLModel) -> PublicationResultGQLModel:
        loader = getLoaders(info).publications
        row = await loader.insert(publication)
        result = PublicationResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="Update the publication.")
    async def publication_update(self, info: strawberryA.types.Info, publication: PublicationUpdateGQLModel) -> PublicationResultGQLModel:
        loader = getLoaders(info).publications
        row = await loader.update(publication)
        result = PublicationResultGQLModel()
        result.msg = "ok"
        result.id = publication.id
        if row is None:
            result.msg = "fail"
            
        return result

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,), mutation=Mutation)
