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

from gql_personalities.GraphResolvers import resolveUserAll, resolveUserById
from gql_personalities.GraphResolvers import resolveRanksForUser, resolveStudiesForUser, resolveMedalsForUser, resolveWorkHistoriesForUser, resolveRelatedDocsForUser
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a user""" )
class UserGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)


    @strawberryA.field(description="""List of ranks for the user""")
    async def ranks(self, info: strawberryA.types.Info) -> typing.List['RankGQLModel']:
        result = await resolveRanksForUser(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(description="""List of studies for the user""")
    async def studies(self, info: strawberryA.types.Info) -> typing.List['StudyGQLModel']:
        result = await resolveStudiesForUser(AsyncSessionFromInfo(info), self.id)
        return result
        
    @strawberryA.field(description="""List of medals for the user""")
    async def medals(self, info: strawberryA.types.Info) -> typing.List['MedalGQLModel']:
        result = await resolveMedalsForUser(AsyncSessionFromInfo(info), self.id)
        return result

    strawberryA.field(description="""List of workHistories for the user""")
    async def workHistories(self, info: strawberryA.types.Info) -> typing.List['WorkHistoryGQLModel']:
        result = await resolveWorkHistoriesForUser(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(description="""List of relatedDocs for the user""")
    async def relatedDocs(self, info: strawberryA.types.Info) -> typing.List['RelatedDocGQLModel']:
        result = await resolveRelatedDocsForUser(AsyncSessionFromInfo(info), self.id)
        return result


from gql_personalities.GraphResolvers import resolveRankAll, resolveRankById
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a rank""")
class RankGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveRankById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
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


from gql_personalities.GraphResolvers import resolveRankTypeAll, resolveRankTypeById
from gql_personalities.GraphResolvers import resolveRankTypeByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a rankType""")
class RankTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveRankTypeById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name


from gql_personalities.GraphResolvers import resolveStudyAll, resolveStudyById
from gql_personalities.GraphResolvers import resolveStudyByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a study""")
class StudyGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveStudyById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
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

from gql_personalities.GraphResolvers import resolveStudyTypeAll, resolveStudyTypeById
from gql_personalities.GraphResolvers import resolveStudyTypeNameByThreeLetters, resolveStudyTypeProgramByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a rankType""")
class StudyTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveStudyTypeById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name

    @strawberryA.field(description="""program""")
    def program(self) -> strawberryA.ID:
        return self.program


from gql_personalities.GraphResolvers import resolveCertificateAll, resolveCertificateById
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a certificate""")
class CertificateGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveCertificateById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
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


from gql_personalities.GraphResolvers import resolveCertificateTypeAll, resolveCertificateTypeById
from gql_personalities.GraphResolvers import resolveCertificateTypeByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a certificateType""")
class CertificateTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveCertificateTypeById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name


from gql_personalities.GraphResolvers import resolveCertificateTypeGroupAll, resolveCertificateTypeGroupById
from gql_personalities.GraphResolvers import resolveCertificateTypeGroupByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a certificateTypeGroup""")
class CertificateTypeGroupGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveCertificateTypeGroupById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name


from gql_personalities.GraphResolvers import resolveMedalAll, resolveMedalById
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a medal""")
class MedalGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveMedalById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""year""")
    def year(self) -> strawberryA.ID:
        return self.year
    
from gql_personalities.GraphResolvers import resolveMedalTypeAll, resolveMedalTypeById
from gql_personalities.GraphResolvers import resolveMedalTypeByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a medalType""")
class MedalTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveMedalTypeById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name


from gql_personalities.GraphResolvers import resolveMedalTypeGroupAll, resolveMedalTypeGroupById
from gql_personalities.GraphResolvers import resolveMedalTypeGroupByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a medalTypeGroup""")
class MedalTypeGroupGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveMedalTypeGroupById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name


from gql_personalities.GraphResolvers import resolveWorkHistoryAll, resolveWorkHistoryById
from gql_personalities.GraphResolvers import resolveWorkHistoryByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a workHistory""")
class WorkHistoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveWorkHistoryById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
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
    def ico(self) -> strawberryA.ID:
        return self.ico


from gql_personalities.GraphResolvers import resolveRelatedDocAll, resolveRelatedDocById 
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a relatedDoc""")
class RelatedDocGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveRelatedDocById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> strawberryA.ID:
        return self.name

    #@strawberryA.field(description="""uploaded""")
    #def uploaded(self) -> strawberryA.ID:
    #    return self.uploaded


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

@strawberryA.type(description="""Type for query root""")
class Query:
#user
    @strawberryA.field(description="""Returns a list of users (paged)""")
    async def user_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[UserGQLModel]:
        result = await resolveUserAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds a User by their id""")
    async def user_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[UserGQLModel, None]:
        result = await resolveUserById(AsyncSessionFromInfo(info), id)
        return result
    
    
#rank
    @strawberryA.field(description="""Returns a list of ranks (paged)""")
    async def rank_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[RankGQLModel]:
        result = await resolveRankAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds a Rank by their id""")
    async def rank_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[RankGQLModel, None]:
        result = await resolveRankById(AsyncSessionFromInfo(info), id)
        return result 

    
#rankTypes
    @strawberryA.field(description="""Returns a list of rankTypes (paged)""")
    async def rankType_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[RankTypeGQLModel]:
        result = await resolveRankTypeAll(AsyncSessionFromInfo(info), skip, limit)
        return result
        
    @strawberryA.field(description="""Finds a rankType by letters, letters should be atleast three""")
    async def rankType_by_letters(self, info: strawberryA.types.Info, validity: Union[bool, None] = None, letters: str = '') -> List[RankTypeGQLModel]:
        result = await resolveRankTypeByThreeLetters(AsyncSessionFromInfo(info), validity, letters)
        return result

    
#study
    @strawberryA.field(description="""Returns a list of studies (paged)""")
    async def study_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[StudyGQLModel]:
        result = await resolveStudyAll(AsyncSessionFromInfo(info), skip, limit)
        return result

#studyTypes
    @strawberryA.field(description="""Returns a list of studyTypes (paged)""")
    async def studyType_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[StudyTypeGQLModel]:
        result = await resolveStudyTypeAll(AsyncSessionFromInfo(info), skip, limit)
        return result
        
    @strawberryA.field(description="""Finds a studyTypeName by letters, letters should be atleast three""")
    async def studyTypeName_by_letters(self, info: strawberryA.types.Info, validity: Union[bool, None] = None, letters: str = '') -> List[StudyTypeGQLModel]:
        result = await resolveStudyTypeNameByThreeLetters(AsyncSessionFromInfo(info), validity, letters)
        return result

    @strawberryA.field(description="""Finds a studyTypeProgram by letters, letters should be atleast three""")
    async def studyTypeProgram_by_letters(self, info: strawberryA.types.Info, validity: Union[bool, None] = None, letters: str = '') -> List[StudyTypeGQLModel]:
        result = await resolveStudyTypeProgramByThreeLetters(AsyncSessionFromInfo(info), validity, letters)
        return result

#certificate
    @strawberryA.field(description="""Returns a list of certificates (paged)""")
    async def certificate_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[CertificateGQLModel]:
        result = await resolveCertificateAll(AsyncSessionFromInfo(info), skip, limit)
        return result


#certificateType
    @strawberryA.field(description="""Returns a list of certificateTypes (paged)""")
    async def certificateType_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[CertificateTypeGQLModel]:
        result = await resolveCertificateTypeAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds a certificateType by letters, letters should be atleast three""")
    async def certificateType_by_letters(self, info: strawberryA.types.Info, validity: Union[bool, None] = None, letters: str = '') -> List[CertificateTypeGQLModel]:
        result = await resolveCertificateTypeByThreeLetters(AsyncSessionFromInfo(info), validity, letters)
        return result


#certificateTypeGroup
    @strawberryA.field(description="""Returns a list of certificateTypeGroups (paged)""")
    async def certificateTypeGroup_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[CertificateTypeGroupGQLModel]:
        result = await resolveCertificateTypeGroupAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds a certificateTypeGroup by letters, letters should be atleast three""")
    async def certificateTypeGroup_by_letters(self, info: strawberryA.types.Info, validity: Union[bool, None] = None, letters: str = '') -> List[CertificateTypeGroupGQLModel]:
        result = await resolveCertificateTypeGroupByThreeLetters(AsyncSessionFromInfo(info), validity, letters)
        return result


#medal
    @strawberryA.field(description="""Returns a list of medals (paged)""")
    async def medal_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[MedalGQLModel]:
        result = await resolveMedalAll(AsyncSessionFromInfo(info), skip, limit)
        return result

#medalType
    @strawberryA.field(description="""Returns a list of medalTypes (paged)""")
    async def medalType_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[MedalTypeGQLModel]:
        result = await resolveMedalTypeAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds a medalType by letters, letters should be atleast three""")
    async def medalType_by_letters(self, info: strawberryA.types.Info, validity: Union[bool, None] = None, letters: str = '') -> List[MedalTypeGQLModel]:
        result = await resolveMedalTypeByThreeLetters(AsyncSessionFromInfo(info), validity, letters)
        return result


#medalTypeGroup
    @strawberryA.field(description="""Returns a list of medalTypeGroups (paged)""")
    async def medalTypeGroup_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[MedalTypeGroupGQLModel]:
        result = await resolveMedalTypeGroupAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds a medalTypeGroup by letters, letters should be atleast three""")
    async def medalTypeGroup_by_letters(self, info: strawberryA.types.Info, validity: Union[bool, None] = None, letters: str = '') -> List[MedalTypeGroupGQLModel]:
        result = await resolveMedalTypeGroupByThreeLetters(AsyncSessionFromInfo(info), validity, letters)
        return result


#workHistory
    @strawberryA.field(description="""Returns a list of workHistories (paged)""")
    async def workHistory_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[WorkHistoryGQLModel]:
        result = await resolveWorkHistoryAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds a workHistory by letters, letters should be atleast three""")
    async def workHistory_by_letters(self, info: strawberryA.types.Info, validity: Union[bool, None] = None, letters: str = '') -> List[WorkHistoryGQLModel]:
        result = await resolveWorkHistoryByThreeLetters(AsyncSessionFromInfo(info), validity, letters)
        return result


#relatedDoc
    @strawberryA.field(description="""Returns a list of relatedDocs (paged)""")
    async def relatedDoc_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[RelatedDocGQLModel]:
        result = await resolveRelatedDocAll(AsyncSessionFromInfo(info), skip, limit)
        return result

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))