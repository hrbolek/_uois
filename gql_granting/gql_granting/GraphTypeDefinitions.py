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

def getLoaders(info):
    return info.context['all']

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

import datetime
@strawberryA.federation.type(
    keys=["id"], description="""Entity representing premade study programs"""
)
class AcProgramGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).acprogram_by_id
        result = await loader.load(id)
        if result is not None:
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

    @strawberryA.field(description="""name""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Bachelor, ...""")
    async def type(self, info: strawberryA.types.Info) -> "AcProgramTypeGQLModel":
        result = await AcProgramTypeGQLModel.resolve_reference(info, self.type_id)
        return result

    @strawberryA.field(description="""primary key""")
    def editor(self) -> "AcProgramEditorGQLModel":
        return self

    @strawberryA.field(description="""subjects in the program""")
    async def subjects(self, info: strawberryA.types.Info) -> List["AcSubjectGQLModel"]:
        loader = getLoaders(info).acsubject_for_program
        result = await loader.load(self.id)
        return result

    #################################################


from gql_granting.GraphResolvers import resolveFormTypeById


@strawberryA.federation.type(
    keys=["id"], description="Program form type (Present, distant, ...)"
)
class AcProgramFormTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).acprogramform_by_id
        result = await loader.load(id)
        if result is not None:
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

    @strawberryA.field(description="primary key")
    def lastchange(self) -> str:
        return self.lastchange


from gql_granting.GraphResolvers import resolveLanguageTypeById


@strawberryA.federation.type(keys=["id"], description="Program language")
class AcProgramLanguageTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).acprogramlanguage_by_id
        result = await loader.load(id)
        if result is not None:
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

    @strawberryA.field(description="primary key")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

from gql_granting.GraphResolvers import resolveLevelTypeById


@strawberryA.federation.type(keys=["id"], description="bachelor, ...")
class AcProgramLevelTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).acprogramlevel_by_id
        result = await loader.load(id)
        if result is not None:
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

    @strawberryA.field(description="primary key")
    def lastchange(self) -> str:
        return self.lastchange


from gql_granting.GraphResolvers import resolveTitleTypeById


@strawberryA.federation.type(keys=["id"], description="Bc., Ing., ...")
class AcProgramTitleTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).acprogramtitle_by_id
        result = await loader.load(id)
        if result is not None:
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

    @strawberryA.field(description="primary key")
    def lastchange(self) -> str:
        return self.lastchange


from gql_granting.GraphResolvers import resolveClassificationTypeById


@strawberryA.federation.type(
    keys=["id"], description="Classification on the end of semesters"
)
class AcClassificationTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).acclassificationtype_by_id
        result = await loader.load(id)
        if result is not None:
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

    @strawberryA.field(description="primary key")
    def lastchange(self) -> str:
        return self.lastchange

from gql_granting.GraphResolvers import resolveLessonTypeById


@strawberryA.federation.type(keys=["id"], description="P, C, LC, S, ...")
class AcLessonTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).aclessontype_by_id
        result = await loader.load(id)
        if result is not None:
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

    @strawberryA.field(description="primary key")
    def lastchange(self) -> str:
        return self.lastchange


###########################################################################################################################
from gql_granting.GraphResolvers import resolveGroupIdsForProgram


@strawberryA.federation.type(keys=["id"], description="Study program editor")
class AcProgramEditorGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).acprogram_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="primary key")
    def id(self) -> strawberryA.ID:
        return self.id

    # change name, add subject, delete subject

    # @strawberryA.field(description="groups linked the program")
    # async def groups(self, info: strawberryA.types.Info) -> List["GroupGQLModel"]:
    #     async with withInfo(info) as session:
    #         links = await resolveGroupIdsForProgram(session, self.id)
    #         result = list(map(lambda item: GroupGQLModel(id=item), links))
    #         return result


###########################################################################################################################

from gql_granting.GraphResolvers import resolveSubjectById, resolveSemestersForSubject
from gql_granting.GraphResolvers import subjectSelect

@strawberryA.federation.type(
    keys=["id"],
    description="""Entity which connects programs and semesters, includes informations about subjects""",
)
class AcSubjectGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).acsubject_by_id
        result = await loader.load(id)
        if result is not None:
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

    @strawberryA.field(description="""name""")
    def lastchange(self) -> str:
        return self.lastchange

    @strawberryA.field(description="""StudyProgramID""")
    async def program(self, info: strawberryA.types.Info) -> "AcProgramGQLModel":
        result = await AcProgramGQLModel.resolve_reference(info, self.program_id)
        return result

    @strawberryA.field(description="""StudyProgramID""")
    async def semesters(
        self, info: strawberryA.types.Info
    ) -> List["AcSemesterGQLModel"]:
        loader = getLoaders(info).acsemester_for_subject
        result = await loader.load(self.id)
        return result


from gql_granting.GraphResolvers import resolveSemesterById, resolveTopicsForSemester


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing each semester in study program"""
)
class AcSemesterGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).acsemester_by_id
        result = await loader.load(id)
        if result is not None:
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

    @strawberryA.field(description="""credits""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange


    # FK###############################################################################################
    @strawberryA.field(description="""SubjectID""")
    async def subject(self, info: strawberryA.types.Info) -> "AcSubjectGQLModel":
        result = await AcSubjectGQLModel.resolve_reference(info, self.subject_id)
        return result

    @strawberryA.field(description="""ClassificationID""")
    async def classifications(
        self, info: strawberryA.types.Info
    ) -> List["AcClassificationGQLModel"]:
        loader = getLoaders(info).acclassification_for_semester
        result = await loader.load(self.id)
        return result

    @strawberryA.field(description="""topics""")
    async def topics(self, info: strawberryA.types.Info) -> List["AcTopicGQLModel"]:
        loader = getLoaders(info).actopics_for_semester
        result = await loader.load(self.id)
        return result


##################################################################################################
from gql_granting.GraphResolvers import resolveClassificationTypeById
from gql_granting.GraphResolvers import resolveTopicById


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity which represents all themes included in semester""",
)
class AcTopicGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).actopic_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name ("Introduction")""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""name ("Introduction")""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""name ("Introduction")""")
    def lastchange(self) -> str:
        return self.lastchange

    @strawberryA.field(description="""order (1)""")
    def order(self) -> Union[int, None]:
        return self.order

    @strawberryA.field(description="""Semester""")
    async def semester(self, info: strawberryA.types.Info) -> "AcSemesterGQLModel":
        result = await AcSemesterGQLModel.resolve_reference(info, self.semester_id)
        return result

    @strawberryA.field(description="""Lessons for a topic""")
    async def lessons(self, info: strawberryA.types.Info) -> List["AcLessonGQLModel"]:
        loader = getLoaders(info).aclessons_for_topic
        result = await loader.load(self.id)
        return result

from gql_granting.GraphResolvers import resolveLessonById


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity which represents all themes included in semester""",
)
class AcLessonGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).aclesson_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""primary key""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    # FK###############################################################################################
    @strawberryA.field(description="""ThemeTypeID""")
    async def type(self, info: strawberryA.types.Info) -> "AcLessonTypeGQLModel":
        result = await AcLessonTypeGQLModel.resolve_reference(info, self.type_id)
        return result

    ##################################################################################################
    @strawberryA.field(description="""number of this lesson in the topic""")
    def count(self) -> int:
        return self.count

    @strawberryA.field(description="""number of this lesson in the topic""")
    async def topic(self, info: strawberryA.types.Info) -> "AcTopicGQLModel":
        result = await AcTopicGQLModel.resolve_reference(info, self.topic_id)
        return result


@strawberryA.federation.type(
    keys=["id"],
    description="""""",
)
class AcProgramTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).acprogramtype_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""primary key""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""primary key""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""primary key""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Bachelor, ...""")
    async def level(self, info: strawberryA.types.Info) -> "AcProgramLevelTypeGQLModel":
        result = await AcProgramLevelTypeGQLModel.resolve_reference(info, self.level_id)
        return result

    @strawberryA.field(description="""Present, Distant, ...""")
    async def form(self, info: strawberryA.types.Info) -> "AcProgramFormTypeGQLModel":
        result = await AcProgramFormTypeGQLModel.resolve_reference(info, self.form_id)
        return result

    @strawberryA.field(description="""Czech, ...""")
    async def language(
        self, info: strawberryA.types.Info
    ) -> "AcProgramLanguageTypeGQLModel":
        result = await AcProgramLanguageTypeGQLModel.resolve_reference(info, self.language_id)
        return result

    @strawberryA.field(description="""Bc., Ing., ...""")
    async def title(self, info: strawberryA.types.Info) -> "AcProgramTitleTypeGQLModel":
        result = await AcProgramTitleTypeGQLModel.resolve_reference(info, self.title_id)
        return result

@strawberryA.federation.type(
    keys=["id"],
    description="""""",
)
class AcClassificationGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).acclassification_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""primary key""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""primary key""")
    async def user(self, info: strawberryA.types.Info) -> "UserGQLModel":
        return UserGQLModel(id=self.user_id)

    @strawberryA.field(description="""primary key""")
    async def semester(self, info: strawberryA.types.Info) -> "AcSemesterGQLModel":
        result = await AcSemesterGQLModel.resolve_reference(info, id=self.semester_id)
        return result

    @strawberryA.field(description="""primary key""")
    async def type(self, info: strawberryA.types.Info) -> "AcClassificationTypeGQLModel":
        result = await AcClassificationTypeGQLModel.resolve_reference(info, id=self.classificationtype_id)
        return result

    @strawberryA.field(description="""primary key""")
    async def level(self, info: strawberryA.types.Info) -> "AcClassificationLevelGQLModel":
        result = await AcClassificationLevelGQLModel.resolve_reference(info, id=self.classificationlevel_id)
        return result

@strawberryA.federation.type(
    keys=["id"],
    description="""""",
)
class AcClassificationLevelGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).acclassificationlevel_by_id
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""primary key""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""primary key""")
    def name_en(self) -> str:
        return self.name_en

from gql_granting.GraphResolvers import resolveLessonTypeById

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


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz

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
from gql_granting.GraphResolvers import programSelect, classificationTypeSelect

@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello_granting(
        self, info: strawberryA.types.Info, id: str
    ) -> Union[str, None]:
        result = f"Hello {id} from granting"
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def program_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcProgramGQLModel", None]:
        result = await AcProgramGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def program_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List["AcProgramGQLModel"]:
        loader = getLoaders(info).acprogram_by_id
        stmt = programSelect.offset(skip).limit(limit)
        result = loader.execute_select(stmt)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def program_type_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcProgramTypeGQLModel", None]:
        result = await AcProgramTypeGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def program_language_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcProgramLanguageTypeGQLModel", None]:
        result = await AcProgramLanguageTypeGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def program_level_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcProgramLevelTypeGQLModel", None]:
        result = await AcProgramLevelTypeGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def program_form_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcProgramFormTypeGQLModel", None]:
        result = await AcProgramFormTypeGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def program_title_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcProgramTitleTypeGQLModel", None]:
        result = await AcProgramTitleTypeGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def acsubject_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcSubjectGQLModel", None]:
        result = await AcSubjectGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def acsemester_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcSemesterGQLModel", None]:
        result = await AcSemesterGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def actopic_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcTopicGQLModel", None]:
        result = await AcTopicGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def aclesson_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcLessonGQLModel", None]:
        result = await AcLessonGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def aclesson_type_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union["AcLessonTypeGQLModel", None]:
        result = await AcLessonTypeGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def acclassification_type_page(
        self, info: strawberryA.types.Info
    ) -> List["AcClassificationTypeGQLModel"]:
        loader = getLoaders(info).acclassificationtype_by_id
        result = await loader.execute_select(classificationTypeSelect)
        return result

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def program_for_group(
        self, info: strawberryA.types.Info, group_id: strawberryA.ID
    ) -> List["AcProgramGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveProgramForGroup(session, id=group_id)
            return result


###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, 
    types=(GroupGQLModel, 
    AcClassificationLevelGQLModel, 
    AcClassificationGQLModel, 
    AcProgramTypeGQLModel, 
    AcClassificationTypeGQLModel, 
    AcProgramTitleTypeGQLModel,
    AcProgramLevelTypeGQLModel,
    AcProgramLanguageTypeGQLModel,
    AcProgramGQLModel,
    AcProgramFormTypeGQLModel))
