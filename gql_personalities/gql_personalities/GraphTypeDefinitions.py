from typing import List, Union
import typing
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


###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################

from gql_personalities.GraphResolvers import (
    resolveRanksForUser,
    resolveStudiesForUser,
    resolveMedalsForUser,
    resolveWorkHistoriesForUser,
    resolveRelatedDocsForUser,
)


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""List of ranks for the user""")
    async def ranks(self, info: strawberryA.types.Info) -> typing.List["RankGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveRanksForUser(session, self.id)
            return result

    @strawberryA.field(description="""List of studies for the user""")
    async def studies(
        self, info: strawberryA.types.Info
    ) -> typing.List["StudyGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveStudiesForUser(session, self.id)
            return result

    @strawberryA.field(description="""List of medals for the user""")
    async def medals(
        self, info: strawberryA.types.Info
    ) -> typing.List["MedalGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveMedalsForUser(session, self.id)
            return result

    strawberryA.field(description="""List of workHistories for the user""")

    async def work_histories(
        self, info: strawberryA.types.Info
    ) -> typing.List["WorkHistoryGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveWorkHistoriesForUser(session, self.id)
            return result

    @strawberryA.field(description="""List of relatedDocs for the user""")
    async def related_docs(
        self, info: strawberryA.types.Info
    ) -> typing.List["RelatedDocGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveRelatedDocsForUser(session, self.id)
            return result


from gql_personalities.GraphResolvers import resolveRankAll, resolveRankById


@strawberryA.federation.type(keys=["id"], description="""Entity representing a rank""")
class RankGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveRankById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""start""")
    def start(self) -> strawberryA.ID:
        return self.start

    @strawberryA.field(description="""end""")
    def end(self) -> strawberryA.ID:
        return self.end

    # TODO RankTypeGQLModel


from gql_personalities.GraphResolvers import resolveRankTypeAll, resolveRankTypeById
from gql_personalities.GraphResolvers import resolveRankTypeByThreeLetters


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a rankType"""
)
class RankTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveRankTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name

    # TODO Ranks Relation


from gql_personalities.GraphResolvers import resolveStudyAll, resolveStudyById
from gql_personalities.GraphResolvers import resolveStudyByThreeLetters


@strawberryA.federation.type(keys=["id"], description="""Entity representing a study""")
class StudyGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveStudyById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""place""")
    def place(self) -> strawberryA.ID:
        return self.place

    @strawberryA.field(description="""program""")
    def program(self) -> strawberryA.ID:
        return self.program

    @strawberryA.field(description="""start""")
    def start(self) -> strawberryA.ID:
        return self.start

    @strawberryA.field(description="""end""")
    def end(self) -> strawberryA.ID:
        return self.end


from gql_personalities.GraphResolvers import (
    resolveCertificateAll,
    resolveCertificateById,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a certificate"""
)
class CertificateGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveCertificateById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""level""")
    def level(self) -> strawberryA.ID:
        return self.level

    @strawberryA.field(description="""validity start""")
    def validity_start(self) -> strawberryA.ID:
        return self.validity_start

    @strawberryA.field(description="""validity end""")
    def validity_end(self) -> strawberryA.ID:
        return self.validity_end


from gql_personalities.GraphResolvers import (
    resolveCertificateTypeAll,
    resolveCertificateTypeById,
)
from gql_personalities.GraphResolvers import resolveCertificateTypeByThreeLetters


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a certificateType"""
)
class CertificateTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveCertificateTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name

    # TODO Certificate Relation


from gql_personalities.GraphResolvers import (
    resolveCertificateTypeGroupAll,
    resolveCertificateTypeGroupById,
)
from gql_personalities.GraphResolvers import resolveCertificateTypeGroupByThreeLetters


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a certificateTypeGroup"""
)
class CertificateTypeGroupGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveCertificateTypeGroupById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name


from gql_personalities.GraphResolvers import resolveMedalAll, resolveMedalById


@strawberryA.federation.type(keys=["id"], description="""Entity representing a medal""")
class MedalGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveMedalById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""year""")
    def year(self) -> strawberryA.ID:
        return self.year


from gql_personalities.GraphResolvers import resolveMedalTypeAll, resolveMedalTypeById
from gql_personalities.GraphResolvers import resolveMedalTypeByThreeLetters


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a medalType"""
)
class MedalTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveMedalTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name


from gql_personalities.GraphResolvers import (
    resolveMedalTypeGroupAll,
    resolveMedalTypeGroupById,
)
from gql_personalities.GraphResolvers import resolveMedalTypeGroupByThreeLetters


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a medalTypeGroup"""
)
class MedalTypeGroupGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveMedalTypeGroupById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name


from gql_personalities.GraphResolvers import (
    resolveWorkHistoryAll,
    resolveWorkHistoryById,
)
from gql_personalities.GraphResolvers import resolveWorkHistoryByThreeLetters


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a workHistory"""
)
class WorkHistoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveWorkHistoryById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""start""")
    def start(self) -> strawberryA.ID:
        return self.start

    @strawberryA.field(description="""end""")
    def end(self) -> strawberryA.ID:
        return self.end

    @strawberryA.field(description="""position""")
    def position(self) -> strawberryA.ID:
        return self.position

    @strawberryA.field(description="""ico""")
    def ico(self) -> Union[strawberryA.ID, None]:
        return self.ico


from gql_personalities.GraphResolvers import resolveRelatedDocAll, resolveRelatedDocById


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a relatedDoc"""
)
class RelatedDocGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveRelatedDocById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name

    # @strawberryA.field(description="""uploaded""")
    # def uploaded(self) -> strawberryA.ID:
    #    return self.uploaded


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################


@strawberryA.type(description="""Type for query root""")
class Query:

    # rank
    @strawberryA.field(description="""Returns a list of ranks (paged)""")
    async def rank_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[RankGQLModel]:
        async with withInfo(info) as session:
            result = await resolveRankAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Finds a Rank by their id""")
    async def rank_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[RankGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveRankById(session, id)
            return result

    # rankTypes
    @strawberryA.field(description="""Returns a list of rankTypes (paged)""")
    async def rankType_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[RankTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveRankTypeAll(session, skip, limit)
            return result

    @strawberryA.field(
        description="""Finds a rankType by letters, letters should be atleast three"""
    )
    async def rankType_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[RankTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveRankTypeByThreeLetters(session, validity, letters)
            return result

    # study
    @strawberryA.field(description="""Returns a list of studies (paged)""")
    async def study_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[StudyGQLModel]:
        async with withInfo(info) as session:
            result = await resolveStudyAll(session, skip, limit)
            return result

    @strawberryA.field(
        description="""Finds a study by letters, letters should be atleast three"""
    )
    async def study_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[StudyGQLModel]:
        async with withInfo(info) as session:
            result = await resolveStudyByThreeLetters(session, validity, letters)
            return result

    # certificate
    @strawberryA.field(description="""Returns a list of certificates (paged)""")
    async def certificate_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[CertificateGQLModel]:
        async with withInfo(info) as session:
            result = await resolveCertificateAll(session, skip, limit)
            return result

    # certificateType
    @strawberryA.field(description="""Returns a list of certificateTypes (paged)""")
    async def certificateType_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[CertificateTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveCertificateTypeAll(session, skip, limit)
            return result

    @strawberryA.field(
        description="""Finds a certificateType by letters, letters should be atleast three"""
    )
    async def certificateType_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[CertificateTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveCertificateTypeByThreeLetters(
                session, validity, letters
            )
            return result

    # certificateTypeGroup
    @strawberryA.field(
        description="""Returns a list of certificateTypeGroups (paged)"""
    )
    async def certificateTypeGroup_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[CertificateTypeGroupGQLModel]:
        async with withInfo(info) as session:
            result = await resolveCertificateTypeGroupAll(session, skip, limit)
        return result

    @strawberryA.field(
        description="""Finds a certificateTypeGroup by letters, letters should be atleast three"""
    )
    async def certificateTypeGroup_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[CertificateTypeGroupGQLModel]:
        async with withInfo(info) as session:
            result = await resolveCertificateTypeGroupByThreeLetters(
                session, validity, letters
            )
            return result

    # medal
    @strawberryA.field(description="""Returns a list of medals (paged)""")
    async def medal_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[MedalGQLModel]:
        async with withInfo(info) as session:
            result = await resolveMedalAll(session, skip, limit)
            return result

    # medalType
    @strawberryA.field(description="""Returns a list of medalTypes (paged)""")
    async def medalType_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[MedalTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveMedalTypeAll(session, skip, limit)
            return result

    @strawberryA.field(
        description="""Finds a medalType by letters, letters should be atleast three"""
    )
    async def medalType_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[MedalTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveMedalTypeByThreeLetters(session, validity, letters)
            return result

    # medalTypeGroup
    @strawberryA.field(description="""Returns a list of medalTypeGroups (paged)""")
    async def medalTypeGroup_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[MedalTypeGroupGQLModel]:
        async with withInfo(info) as session:
            result = await resolveMedalTypeGroupAll(session, skip, limit)
            return result

    @strawberryA.field(
        description="""Finds a medalTypeGroup by letters, letters should be atleast three"""
    )
    async def medalTypeGroup_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[MedalTypeGroupGQLModel]:
        async with withInfo(info) as session:
            result = await resolveMedalTypeGroupByThreeLetters(
                session, validity, letters
            )
            return result

    # workHistory
    @strawberryA.field(description="""Returns a list of workHistories (paged)""")
    async def workHistory_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[WorkHistoryGQLModel]:
        async with withInfo(info) as session:
            result = await resolveWorkHistoryAll(session, skip, limit)
            return result

    @strawberryA.field(
        description="""Finds a workHistory by letters, letters should be atleast three"""
    )
    async def workHistory_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[WorkHistoryGQLModel]:
        async with withInfo(info) as session:
            result = await resolveWorkHistoryByThreeLetters(session, validity, letters)
            return result

    # relatedDoc
    @strawberryA.field(description="""Returns a list of relatedDocs (paged)""")
    async def relatedDoc_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[RelatedDocGQLModel]:
        async with withInfo(info) as session:
            result = await resolveRelatedDocAll(session, skip, limit)
            return result


###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,))
