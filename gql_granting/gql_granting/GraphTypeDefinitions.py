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

from gql_granting.GraphResolvers import resolveSemesterByID, resolveSubjectByID, resolveClassificationByID, \
    resolveThemeTypeByID, resolveStudyThemeByID, resolveStudyProgramByID, resolveStudyLanguageByID, \
    resolveStudyThemeItemByID, resolveThemesforSemester, resolveSubjectsforProgram, resolveSemestersforSubject, \
    resolveSubjectsforLanguage, resolveThemesforSemester


@strawberryA.federation.type(keys=["id"], description="""Entity representing premade study programs""")
class StudyProgramGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveStudyProgramByID(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""type""")
    def type(self) -> str:
        return self.type

    @strawberryA.field(description="""study duration""")
    def study_duration(self) -> int:
        return self.study_duration

    @strawberryA.field(description="""type of study""")
    def type_of_study(self) -> str:
        return self.type_of_study

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime:
        return self.lastchange

    @strawberryA.field(description="""primary key""")
    def editor(self) -> 'StudyProgramEditorGQLModel':
        return self

    # FK ################################################
    @strawberryA.field(description="""SemestersforSubject""")
    async def themes(self, info: strawberryA.types.Info) -> List['SubjectGQLModel']:
        result = await resolveSubjectsforProgram(AsyncSessionFromInfo(info), self.id)
        return result


####################################################################################

###########################################################################################################################
"""""
@strawberryA.federation.type(keys=["id"], description="Study program editor")
class StudyProgramEditorGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveStudyProgramByID(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="primary key")
    def id(self) -> strawberryA.ID:
        return self.id
    # change name, program, add subject, delete subject
"""""


###########################################################################################################################


@strawberryA.federation.type(keys=["id"],
                             description="""Entity which connects programs and semesters, includes informations about subjects""")
class SubjectGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveSubjectByID(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime:
        return self.lastchange

    # FK###############################################################################################
    @strawberryA.field(description="""StudyProgramID""")
    async def study_program(self, info: strawberryA.types.Info) -> 'StudyProgramGQLModel':
        result = await resolveStudyProgramByID(AsyncSessionFromInfo(info), self.studyProgram_id)
        return result

    @strawberryA.field(description="""StudyLanguageID""")
    async def study_language(self, info: strawberryA.types.Info) -> 'StudyLanguageGQLModel':
        result = await resolveStudyLanguageByID(AsyncSessionFromInfo(info), self.studyLanguage_id)
        return result

    @strawberryA.field(description="""SemestersforSubject""")
    async def themes(self, info: strawberryA.types.Info) -> List['SemesterGQLModel']:
        result = await resolveSemestersforSubject(AsyncSessionFromInfo(info), self.id)
        return result


##################################################################################################
@strawberryA.federation.type(keys=["id"], description="""Entity representing each semester in study program""")
class StudyLanguageGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveStudyLanguageByID(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime:
        return self.lastchange

    # FK #############################################################################
    @strawberryA.field(description="""SubjectsforLanguage""")
    async def subjects(self, info: strawberryA.types.Info) -> List['SubjectGQLModel']:
        result = await resolveSubjectsforLanguage(AsyncSessionFromInfo(info), self.id)
        return result

    ################################################################################


@strawberryA.federation.type(keys=["id"], description="""Entity representing each semester in study program""")
class SemesterGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveSemesterByID(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""semester number""")
    def semester_number(self) -> int:
        return self.semester_number

    @strawberryA.field(description="""credits""")
    def credits(self) -> int:
        return self.credits

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime:
        return self.lastchange

    # FK###############################################################################################
    @strawberryA.field(description="""SubjectID""")
    async def subject(self, info: strawberryA.types.Info) -> 'SubjectGQLModel':
        result = await resolveSubjectByID(AsyncSessionFromInfo(info), self.subject_id)
        return result

    @strawberryA.field(description="""ClassificationID""")
    async def classification(self, info: strawberryA.types.Info) -> 'ClassificationGQLModel':
        result = await resolveClassificationByID(AsyncSessionFromInfo(info), self.classification_id)
        return result

    @strawberryA.field(description="""ThemesfromSemester""")
    async def themes(self, info: strawberryA.types.Info) -> List['StudyThemeGQLModel']:
        result = await resolveThemesforSemester(AsyncSessionFromInfo(info), self.id)
        return result


##################################################################################################
@strawberryA.federation.type(keys=["id"], description="""Entity representing each semester in study program""")
class ClassificationGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveClassificationByID(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime:
        return self.lastchange

# FK#############################################################################

#################################################################################
@strawberryA.federation.type(keys=["id"], description="""Entity which represents all themes included in semester""")
class StudyThemeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveStudyThemeByID(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""SemesterID""")
    async def semester(self, info: strawberryA.types.Info) -> 'SemesterGQLModel':
        result = await resolveSemesterByID(AsyncSessionFromInfo(info), self.Semester_id)
        return result

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime:
        return self.lastchange


@strawberryA.federation.type(keys=["id"], description="""Entity which represents all themes included in semester""")
class StudyThemeItemGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveStudyThemeItemByID(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime:
        return self.lastchange

    # FK###############################################################################################
    @strawberryA.field(description="""StudyThemeID""")
    async def study_theme(self, info: strawberryA.types.Info) -> 'StudyLanguageGQLModel':
        result = await resolveStudyThemeByID(AsyncSessionFromInfo(info), self.studyTheme_id)
        return result

    @strawberryA.field(description="""ThemeTypeID""")
    async def theme_type(self, info: strawberryA.types.Info) -> 'ThemeTypeGQLModel':
        result = await resolveThemeTypeByID(AsyncSessionFromInfo(info), self.themeType_id)
        return result

    ##################################################################################################
    @strawberryA.field(description="""lessons""")
    def lessons(self) -> int:
        return self.lessons


@strawberryA.federation.type(keys=["id"], description="""Entity which represents all themes included in semester""")
class ThemeTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveThemeTypeByID(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""lastchange""")
    def lastchange(self) -> datetime:
        return self.lastchange


###########################################################################################################################
#
# priklad rozsireni UserGQLModel
#
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz


#     zde je rozsireni o dalsi resolvery
#     @strawberryA.field(description="""Inner id""")
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(AsyncSessionFromInfo(info), self.id)
#         return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

@strawberryA.type(description="""Type for query root""")
class Query:

    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result


# byID, page

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,))
