from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
import datetime
from typing import List, Union, Optional
from pydoc import resolve

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
#   EDITOR
#
###########################################################################################################################
@strawberryA.input
class UserUpdateGQLModel:
    lastchange: datetime.datetime #razitko

    rank: Optional[uuid.UUID] = None
    study: Optional[uuid.UUID] = None
    certificate: Optional[uuid.UUID] = None
    medal: Optional[uuid.UUID] = None
    workHistory: Optional[uuid.UUID] = None
    relatedDoc: Optional[uuid.UUID] = None


@strawberryA.input
class UserInsertGQLModel:
    id: Optional[uuid.UUID] = None

    rank: Optional[uuid.UUID] = None
    study: Optional[uuid.UUID] = None
    certificate: Optional[uuid.UUID] = None
    medal: Optional[uuid.UUID] = None
    workHistory: Optional[uuid.UUID] = None
    relatedDoc: Optional[uuid.UUID] = None


@strawberryA.federation.type(keys=["id"], extend=True)
class UserEditorGQLModel:
    ##
    ## Mutace, obejiti problemu s federativnim API
    ##
    
    # vysledky opearace update
    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveUserById(session, id)
            #result = await resolveUserById(AsyncSessionFromInfo(info), id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    async def user(self, info: strawberryA.types.Info) -> 'UserGQLModel':
        #result = await resolveUserById(AsyncSessionFromInfo(info), self.id)
        async with withInfo(info) as session:
            result = await resolveUserById(session, self.id)
            return result

    @strawberryA.field(description="""Updates the user data""")
    async def update(self, info: strawberryA.types.Info, data: UserUpdateGQLModel) -> 'UserEditorGQLModel':
        lastchange = data.lastchange
        #await resolverUpdateUser(AsyncSessionFromInfo(info), id=self.id, data=data)
        async with withInfo(info) as session:
            #await resolverUpdateUser(session, id=self.id, data=data)
            if (lastchange == data.lastchange):
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = UserEditorGQLModel()
            result.id = self.id

            if(data == data.rank):
                result = resolveRanksForUser
            
            result.result = resultMsg
            return result


###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################

#from gql_personalities.GraphResolvers import resolveUserById
from gql_personalities.GraphResolvers import resolveRanksForUser, resolveStudiesForUser, resolveMedalsForUser, resolveWorkHistoriesForUser, resolveRelatedDocsForUser
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    """
    class representing UserModel
    """

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveUserById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result
        
    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""List of ranks for the user""")
    async def ranks(self, info: strawberryA.types.Info) -> typing.List["RankGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveRanksForUser(session, self.id)
            return result

    @strawberryA.field(description="""List of studies for the user""")
    async def studies(
        self, info: strawberryA.types.Info) -> typing.List["StudyGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveStudiesForUser(session, self.id)
            return result

    @strawberryA.field(description="""List of medals for the user""")
    async def medals(
        self, info: strawberryA.types.Info) -> typing.List["MedalGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveMedalsForUser(session, self.id)
            return result

    @strawberryA.field(description="""List of workHistories for the user""")
    async def workHistories(
        self, info: strawberryA.types.Info) -> typing.List["WorkHistoryGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveWorkHistoriesForUser(session, self.id)
            return result

    @strawberryA.field(description="""List of relatedDocs for the user""")
    async def relatedDocs(
        self, info: strawberryA.types.Info) -> typing.List["RelatedDocGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveRelatedDocsForUser(session, self.id)
            return result




from gql_personalities.GraphResolvers import resolveRankAll, resolveRankById
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a rank""")
class RankGQLModel:
    """
    class representing rank

    Attributes
    ----------
    id: UUID(UUID4)
        primary key of rank
    user_id: UUIDFKey(UUID4)
        id of user
    rankType_id: ForeignKey personalitiesranktypes_id
        id of rankType for rank
    start: datetime
        date when was rank acquired
    end: datetime
        date when was rank lost
    created: datetime
        date when rank was created in db
    lastchange: datetime
        date when rank was last changed in db
    changedby: UUIDFKey
        who made the last change
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveRankById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""foreign key""")
    def user_id(self) -> strawberryA.ID:
        return self.user_id
    
    @strawberryA.field(description="""foreign key""")
    def rankType_id(self) -> strawberryA.ID:
        return self.rankType_id

    @strawberryA.field(description="""start""")
    def start(self) -> datetime.datetime:
        return self.start

    @strawberryA.field(description="""end""")
    def end(self) -> datetime.datetime:
        return self.end

    @strawberryA.field(description="""created""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""foreign key""")
    def changedby(self) -> strawberryA.ID:
        return self.changedby



from gql_personalities.GraphResolvers import resolveRankTypeAll, resolveRankTypeById
from gql_personalities.GraphResolvers import resolveRankTypeByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a rankType""")
class RankTypeGQLModel:
    """
    class representing rankType

    Attributes
    ----------
    id: UUID(UUID4)
        primary key of rankType for rank
    name: str
        name of rankType
    created: datetime
        date when rankType was created in db
    lastchange: datetime
        date when rankType was last changed in db
    changedby: UUIDFKey
        who made the last change
    """
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
    def name(self) -> str:
        return self.name
    
    @strawberryA.field(description="""created""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""foreign key""")
    def changedby(self) -> strawberryA.ID:
        return self.changedby





from gql_personalities.GraphResolvers import resolveStudyAll, resolveStudyById
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a study""")
class StudyGQLModel:
    """
    class representing study

    Attributes
    ----------
    id: UUID(UUID4)
        primary key of study
    user_id: UUIDFKey
        id of user
    studyType_id: foreign key
        id of studyType for study
    start: datetime
        date when studying started
    end: datetime
        date when studying stopped
    created: datetime
        date when study was created in db
    lastchange: datetime
        date when study was last changed in db
    changedby: UUIDFKey
        who made the last change
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveStudyById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""foreign key""")
    def user_id(self) -> strawberryA.ID:
        return self.user_id
    
    @strawberryA.field(description="""foreign key""")
    def studyType_id(self) -> strawberryA.ID:
        return self.studyType_id

    @strawberryA.field(description="""start""")
    def start(self) -> datetime.datetime:
        return self.start

    @strawberryA.field(description="""end""")
    def end(self) -> datetime.datetime:
        return self.end
    
    @strawberryA.field(description="""created""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""foreign key""")
    def changedby(self) -> strawberryA.ID:
        return self.changedby





from gql_personalities.GraphResolvers import resolveStudyTypeAll, resolveStudyTypeById
from gql_personalities.GraphResolvers import resolveStudyTypeNameByThreeLetters, resolveStudyTypeProgramByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a rankType""")
class StudyTypeGQLModel:
    """
    class representing studyType

    Attributes
    ----------
    id: UUID(UUID4)
        primary key of studyType for study
    name: str
        name of school
    program: str
        name of studying program
    created: datetime
        date when studyType was created in db
    lastchange: datetime
        date when studyType was last changed in db
    changedby: UUIDFKey
        who made the last change
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveStudyTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""program""")
    def program(self) -> str:
        return self.program

    @strawberryA.field(description="""created""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""foreign key""")
    def changedby(self) -> strawberryA.ID:
        return self.changedby



from gql_personalities.GraphResolvers import resolveCertificateAll, resolveCertificateById
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a certificate""")
class CertificateGQLModel:
    """
    class representing certificate

    Attributes
    ----------
    id: UUID(UUID4)
        primary key of certificate
    user_id: UUIDFKey
        id of user
    certificateType_id: foreign key
        id of certificateType for certificate
    level: str
        level of certificate
    validity_start: datetime
        date when certificate became valid
    validity_end: datetime
        date when certificate became invalid
    created: datetime
        date when certificate was created in db
    lastchange: datetime
        date when certificate was last changed in db
    changedby: UUIDFKey
        who made the last change
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveCertificateById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return 

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""foreign key""")
    def user_id(self) -> strawberryA.ID:
        return self.user_id
    
    @strawberryA.field(description="""foreign key""")
    def certificateType_id(self) -> strawberryA.ID:
        return self.certificateType_id
    
    @strawberryA.field(description="""level""")
    def level(self) -> str:
        return self.level

    @strawberryA.field(description="""validity start""")
    def validity_start(self) -> datetime.datetime:
        return self.validity_start

    @strawberryA.field(description="""validity end""")
    def validity_end(self) -> datetime.datetime:
        return self.validity_end
    
    @strawberryA.field(description="""created""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""foreign key""")
    def changedby(self) -> strawberryA.ID:
        return self.changedby





from gql_personalities.GraphResolvers import resolveCertificateTypeAll, resolveCertificateTypeById
from gql_personalities.GraphResolvers import resolveCertificateTypeByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a certificateType""")
class CertificateTypeGQLModel:
    """
    class representing StudyTypeModel

    Attributes
    ----------
    id: UUID(UUID4)
        primary key of studyType for study
    certificateTypeGroup_id: foreign key
        foreign key of certificateTypeGroup for certificateType
    name: str
        czech name of certificateType
    name_en: str
        english name of certificateType
    created: datetime
        date when certificateType was created in db
    lastchange: datetime
        date when certificateType was last changed in db
    changedby: UUIDFKey
        who made the last change
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveCertificateTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""foreign key""")
    def certificateTypeGroup_id(self) -> strawberryA.ID:
        return self.certificateTypeGroup_id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name
    
    @strawberryA.field(description="""name_en""")
    def name_en(self) -> str:
        return self.name_en
    
    @strawberryA.field(description="""created""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""foreign key""")
    def changedby(self) -> strawberryA.ID:
        return self.changedby





from gql_personalities.GraphResolvers import resolveCertificateTypeGroupAll, resolveCertificateTypeGroupById
from gql_personalities.GraphResolvers import resolveCertificateTypeGroupByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a certificateTypeGroup""")
class CertificateTypeGroupGQLModel:
    """
    class representing CertificateTypeGroup

    Attributes
    ----------
    id: UUID(UUID4)
        primary key of CertificateTypeGroup for CertificateType
    name: str
        czech name of CertificateTypeGroup
    name_en: str
        english name of CertificateTypeGroup
    created: datetime
        date when certificateTypeGroup was created in db
    lastchange: datetime
        date when certificateTypeGroup was last changed in db
    changedby: UUIDFKey
        who made the last change
    """
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
    def name(self) -> str:
        return self.name
    
    @strawberryA.field(description="""name_en""")
    def name_en(self) -> str:
        return self.name_en
    
    @strawberryA.field(description="""created""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""foreign key""")
    def changedby(self) -> strawberryA.ID:
        return self.changedby





from gql_personalities.GraphResolvers import resolveMedalAll, resolveMedalById
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a medal""")
class MedalGQLModel:
    """
    class representing medal

    Attributes
    ----------
    id: UUID(UUID4)
        primary key of medal
    user_id: UUIDFKey
        id of user
    medalType_id: foreign key
        id of medalType for medal
    year: int
        year when medal was acquired
    created: datetime
        date when medal was created in db
    lastchange: datetime
        date when medal was last changed in db
    changedby: UUIDFKey
        who made the last change
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveMedalById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""foreign key""")
    def user_id(self) -> strawberryA.ID:
        return self.user_id
    
    @strawberryA.field(description="""foreign key""")
    def medalType_id(self) -> strawberryA.ID:
        return self.medalType_id
    
    @strawberryA.field(description="""year""")
    def year(self) -> int:
        return self.year
    
    @strawberryA.field(description="""created""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""foreign key""")
    def changedby(self) -> strawberryA.ID:
        return self.changedby
    

    
from gql_personalities.GraphResolvers import resolveMedalTypeAll, resolveMedalTypeById
from gql_personalities.GraphResolvers import resolveMedalTypeByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a medalType""")
class MedalTypeGQLModel:
    """
    class representing medalType

    Attributes
    ----------
    id: UUID(UUID4)
        primary key of medalType
    medalTypeGroup_id: foreign key
        id of medalTypeGroup for medalType
    name: str
        name of medalType
    created: datetime
        date when medalType was created in db
    lastchange: datetime
        date when medalType was last changed in db
    changedby: UUIDFKey
        who made the last change
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveMedalTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""foreign key""")
    def medalTypeGroup_id(self) -> strawberryA.ID:
        return self.medalTypeGroup_id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name
    
    @strawberryA.field(description="""created""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""foreign key""")
    def changedby(self) -> strawberryA.ID:
        return self.changedby
    




from gql_personalities.GraphResolvers import resolveMedalTypeGroupAll, resolveMedalTypeGroupById
from gql_personalities.GraphResolvers import resolveMedalTypeGroupByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a medalTypeGroup""")
class MedalTypeGroupGQLModel:
    """
    class representing medalTypeGroup

    Attributes
    ----------
    id: UUID(UUID4)
        primary key of medalTypeGroup
    name: str
        name of medalTypeGroup
    created: datetime
        date when medalTypeGroup was created in db
    lastchange: datetime
        date when medalTypeGroup was last changed in db
    changedby: UUIDFKey
        who made the last change
    """
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
    
    @strawberryA.field(description="""created""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""foreign key""")
    def changedby(self) -> strawberryA.ID:
        return self.changedby




from gql_personalities.GraphResolvers import resolveWorkHistoryAll, resolveWorkHistoryById
from gql_personalities.GraphResolvers import resolveWorkHistoryByThreeLetters
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a workHistory""")
class WorkHistoryGQLModel:
    """
    class representing workHistory

    Attributes
    ----------
    id: UUID(UUID4)
        primary key of workHistory
    user_id: UUIDFKey
        id of user
    start: datetime
        date when user started working
    end: datetime
        date when user stopped working
    position: str
        what type of position is the work about
    ico: str
        ico of employer
    created: datetime
        date when study was created in db
    lastchange: datetime
        date when study was last changed in db
    changedby: UUIDFKey
        who made the last change
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveWorkHistoryById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""foreign key""")
    def user_id(self) -> strawberryA.ID:
        return self.user_id

    @strawberryA.field(description="""start""")
    def start(self) -> datetime.datetime:
        return self.start

    @strawberryA.field(description="""end""")
    def end(self) -> datetime.datetime:
        return self.end

    @strawberryA.field(description="""position""")
    def position(self) -> str:
        return self.position

    @strawberryA.field(description="""ico""")
    def ico(self) -> str:
        return self.ico
    
    @strawberryA.field(description="""created""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""foreign key""")
    def changedby(self) -> strawberryA.ID:
        return self.changedby




from gql_personalities.GraphResolvers import resolveRelatedDocAll, resolveRelatedDocById 
@strawberryA.federation.type(extend=True, keys=["id"], description="""Entity representing a relatedDoc""")
class RelatedDocGQLModel:
    """
    class representing relatedDoc

    Attributes
    ----------
    id: UUID(UUID4)
        primary key of workHistory
    user_id: UUIDFKey
        id of user
    name: str
        name of document
    created: datetime
        date when study was created in db
    lastchange: datetime
        date when study was last changed in db
    changedby: UUIDFKey
        who made the last change
    """
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveRelatedDocById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""foreign key""")
    def user_id(self) -> strawberryA.ID:
        return self.user_id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name
    
    @strawberryA.field(description="""created""")
    def created(self) -> datetime.datetime:
        return self.created

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    
    @strawberryA.field(description="""foreign key""")
    def changedby(self) -> strawberryA.ID:
        return self.changedby

    #@strawberryA.field(description="""uploaded""")
    #def uploaded(self) -> strawberryA.ID:
    #    return self.uploaded


###########################################################################################################################
#
#           Query model
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
    @strawberryA.field(
            description="""Returns a list of studies (paged)"""
    )
    async def study_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[StudyGQLModel]:
        async with withInfo(info) as session:
            result = await resolveStudyAll(session, skip, limit)
            return result

# studyTypes
    @strawberryA.field(
            description="""Returns a list of studyTypes (paged)"""
    )
    async def studyType_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[StudyTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveStudyTypeAll(session, skip, limit)
            return result
        
    @strawberryA.field(
            description="""Finds a studyTypeName by letters, letters should be atleast three"""
    )
    async def studyTypeName_by_letters(
        self, 
        info: strawberryA.types.Info, 
        validity: Union[bool, None] = None, 
        letters: str = ""
    ) -> List[StudyTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveStudyTypeNameByThreeLetters(session, validity, letters)
            return result

    @strawberryA.field(
            description="""Finds a studyTypeProgram by letters, letters should be atleast three"""
    )
    async def studyTypeProgram_by_letters(
        self, 
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None, 
        letters: str = ""
    ) -> List[StudyTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveStudyTypeProgramByThreeLetters(session, validity, letters)
            return result

# certificate
    @strawberryA.field(description="""Returns a list of certificates (paged)""")
    async def certificate_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[CertificateGQLModel]:
        async with withInfo(info) as session:
            result = await resolveCertificateAll(session, skip, limit)
            return 

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
        
        
schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, UserEditorGQLModel))