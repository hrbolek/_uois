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
    return info.context["session"]


###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#

# from gql_granting.GraphResolvers import resolveSemesterByID, resolveSubjectByID, resolveClassificationByID, \
#    resolveThemeTypeByID, resolveStudyThemeByID, resolveStudyProgramByID, resolveStudyLanguageByID, \
#    resolveStudyThemeItemByID

from gql_granting.GraphResolvers import (
    resolveProgramById,
    resolveFormTypeById,
    resolveLanguageTypeById,
    resolveLevelTypeById,
    resolveTitleTypeById,
    resolveSubjectsForProgram,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing premade study programs"""
)
class AcProgramGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveProgramById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""Bachelor, ...""")
    async def level(self, info: strawberryA.types.Info) -> "AcProgramLevelTypeGQLModel":
        async with withInfo(info) as session:
            result = await resolveLevelTypeById(session, self.level_id)
            return result

    @strawberryA.field(description="""Present, Distant, ...""")
    async def form(self, info: strawberryA.types.Info) -> "AcProgramFormTypeGQLModel":
        async with withInfo(info) as session:
            result = await resolveFormTypeById(session, self.form_id)
            return result

    @strawberryA.field(description="""Czech, ...""")
    async def language(
        self, info: strawberryA.types.Info
    ) -> "AcProgramLanguageTypeGQLModel":
        async with withInfo(info) as session:
            result = await resolveLanguageTypeById(session, self.language_id)
            return result

    @strawberryA.field(description="""Bc., Ing., ...""")
    async def title(self, info: strawberryA.types.Info) -> "AcProgramTitleTypeGQLModel":
        async with withInfo(info) as session:
            result = await resolveTitleTypeById(session, self.title_id)
            return result

    @strawberryA.field(description="""primary key""")
    def editor(self) -> "AcProgramEditorGQLModel":
        return self

    async def subjects(self, info: strawberryA.types.Info) -> List["AcSubjectGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveSubjectsForProgram(session, self.title_id)
            return result

    #################################################


@strawberryA.federation.type(keys=["id"], description="Study program editor")
class AcProgramEditorGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveProgramById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="primary key")
    def id(self) -> strawberryA.ID:
        return self.id


from gql_granting.GraphResolvers import resolveFormTypeById


@strawberryA.federation.type(
    keys=["id"], description="Program form type (Present, distant, ...)"
)
class AcProgramFormTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveFormTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="primary key")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="primary key")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="primary key")
    def name_en(self) -> str:
        return self.name_en


from gql_granting.GraphResolvers import resolveLanguageTypeById


@strawberryA.federation.type(keys=["id"], description="Program language")
class AcProgramLanguageTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveLanguageTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="primary key")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="primary key")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="primary key")
    def name_en(self) -> str:
        return self.name_en


from gql_granting.GraphResolvers import resolveLevelTypeById


@strawberryA.federation.type(keys=["id"], description="bachelor, ...")
class AcProgramLevelTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveLevelTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="primary key")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="primary key")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="primary key")
    def name_en(self) -> str:
        return self.name_en


from gql_granting.GraphResolvers import resolveTitleTypeById


@strawberryA.federation.type(keys=["id"], description="Bc., Ing., ...")
class AcProgramTitleTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveTitleTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="primary key")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="primary key")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="primary key")
    def name_en(self) -> str:
        return self.name_en


from gql_granting.GraphResolvers import resolveClassificationTypeById


@strawberryA.federation.type(
    keys=["id"], description="Classification on the end of semesters"
)
class AcClassificationTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveClassificationTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="primary key")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="primary key")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="primary key")
    def name_en(self) -> str:
        return self.name_en


from gql_granting.GraphResolvers import resolveLessonTypeById


@strawberryA.federation.type(keys=["id"], description="P, C, LC, S, ...")
class AcLessonTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveLessonTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="primary key")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="primary key")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="primary key")
    def name_en(self) -> str:
        return self.name_en


###########################################################################################################################
from gql_granting.GraphResolvers import resolveGroupIdsForProgram


@strawberryA.federation.type(keys=["id"], description="Study program editor")
class AcProgramEditorGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveProgramById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="primary key")
    def id(self) -> strawberryA.ID:
        return self.id

    # change name, add subject, delete subject

    @strawberryA.field(description="groups linked the program")
    async def groups(self, info: strawberryA.types.Info) -> List["GroupGQLModel"]:
        async with withInfo(info) as session:
            links = await resolveGroupIdsForProgram(session, self.id)
            result = list(map(lambda item: GroupGQLModel(id=item), links))
            return result


###########################################################################################################################

from gql_granting.GraphResolvers import resolveSubjectById, resolveSemestersForSubject


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity which connects programs and semesters, includes informations about subjects""",
)
class AcSubjectGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveSubjectById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name

    # FK###############################################################################################
    @strawberryA.field(description="""StudyProgramID""")
    async def program(self, info: strawberryA.types.Info) -> "AcProgramGQLModel":
        async with withInfo(info) as session:
            result = await resolveProgramById(session, self.program_id)
            return result

    @strawberryA.field(description="""StudyProgramID""")
    async def semesters(
        self, info: strawberryA.types.Info
    ) -> List["AcSemesterGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveSemestersForSubject(session, self.program_id)
            return result


from gql_granting.GraphResolvers import resolveSemesterById, resolveTopicsForSemester


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing each semester in study program"""
)
class AcSemesterGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveSemesterById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""semester number""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""credits""")
    def credits(self) -> int:
        return self.credits

    # FK###############################################################################################
    @strawberryA.field(description="""SubjectID""")
    async def subject(self, info: strawberryA.types.Info) -> "AcSubjectGQLModel":
        async with withInfo(info) as session:
            result = await resolveSubjectById(session, self.subject_id)
            return result

    @strawberryA.field(description="""ClassificationID""")
    async def classification(
        self, info: strawberryA.types.Info
    ) -> "ClassificationTypeGQLModel":
        async with withInfo(info) as session:
            result = await resolveClassificationTypeById(
                session, self.classificationtype_id
            )
            return result

    @strawberryA.field(description="""topics""")
    async def topics(self, info: strawberryA.types.Info) -> List["AcTopicGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveTopicsForSemester(session, self.classificationtype_id)
            return result


##################################################################################################
from gql_granting.GraphResolvers import resolveClassificationTypeById


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing each semester in study program"""
)
class ClassificationTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveClassificationTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name


from gql_granting.GraphResolvers import resolveTopicById


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity which represents all themes included in semester""",
)
class AcTopicGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveTopicById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name ("Introduction")""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""order (1)""")
    def order(self) -> Union[int, None]:
        return self.order

    @strawberryA.field(description="""Semester""")
    async def semester(self, info: strawberryA.types.Info) -> "AcSemesterGQLModel":
        async with withInfo(info) as session:
            result = await resolveSemesterById(session, self.semester_id)
            return result

    @strawberryA.field(description="""Lessons for a topic""")
    async def lessons(self, info: strawberryA.types.Info) -> List["AcLessonGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveSemesterById(session, self.semester_id)
            return result


from gql_granting.GraphResolvers import resolveLessonById


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity which represents all themes included in semester""",
)
class AcLessonGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveLessonById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    # FK###############################################################################################
    @strawberryA.field(description="""ThemeTypeID""")
    async def type(self, info: strawberryA.types.Info) -> "AcLessonTypeGQLModel":
        async with withInfo(info) as session:
            result = await resolveLessonTypeById(session, self.type_id)
            return result

    ##################################################################################################
    @strawberryA.field(description="""number of this lesson in the topic""")
    def count(self) -> int:
        return self.count

    @strawberryA.field(description="""number of this lesson in the topic""")
    async def topic(self, info: strawberryA.types.Info) -> "AcTopicGQLModel":
        async with withInfo(info) as session:
            result = await resolveTopicById(session, self.topic_id)
            return result


from gql_granting.GraphResolvers import resolveLessonTypeById


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity which represents all themes included in semester""",
)
class AcLessonTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveLessonTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name (P, C, LC, ...)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""english name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""abbreviation (P, C, LC, ...)""")
    def abbr(self) -> str:
        return self.abbr


###########################################################################################################################
#
# priklad rozsireni GroupGQLModel
#
from gql_granting.GraphResolvers import resolveProgramForGroup, resolveJSONForProgram


@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz

    async def program(
        self, info: strawberryA.types.Info
    ) -> Union["AcProgramGQLModel", None]:
        async with withInfo(info) as session:
            result = await resolveProgramForGroup(session, id)
            return result


#     zde je rozsireni o dalsi resolvery
#     @strawberryA.field(description="""Inner id""")
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(session,self.id)
#         return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
from typing import Any, NewType

JSON = strawberryA.scalar(
    NewType("JSON", object),
    description="The `JSON` scalar type represents JSON values as specified by ECMA-404",
    serialize=lambda v: v,
    parse_value=lambda v: v,
)

from gql_granting.GraphResolvers import resolveProgramPage, resolveProgramForGroup


@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello_granting(
        self, info: strawberryA.types.Info, id: str
    ) -> Union[str, None]:
        result = f"Hello {id} from granting"
        return result

    async def program_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List["AcProgramGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveProgramPage(session, skip=skip, limit=limit)
            return result

    async def program_for_group(
        self, info: strawberryA.types.Info, group_id: strawberryA.ID
    ) -> List["AcProgramGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveProgramForGroup(session, id=group_id)
            return result

    async def program_json(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["JSON", None]:
        async with withInfo(info) as session:
            result = await resolveJSONForProgram(session, id)
            return result


###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(GroupGQLModel,))
