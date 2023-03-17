from typing import List, Union, Optional
import typing
from unittest import result
import strawberry as strawberryA
import uuid
import datetime
from contextlib import asynccontextmanager


@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context['asyncSessionMaker']
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


def AsyncSessionFromInfo(info):
    return info.context['session']


def AsyncSessionMakerFromInfo(info):
    return info.context['asyncSessionMaker']


###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#

from gql_granting.GraphResolvers import resolveSemesterByID, resolveSubjectByID, resolveClassificationByID, \
    resolveThemeTypeByID, resolveStudyThemeByID, resolveStudyProgramByID, resolveStudyLanguageByID, \
    resolveStudyThemeItemByID, resolveThemesforSemester, resolveSubjectsforProgram, resolveSemestersforSubject, \
    resolveSubjectsforLanguage, resolveThemesforSemester, resolveStudyProgramAll, resolveSubjectAll, resolveLanguageAll, resolveSemesterAll, resolveClassificationAll, resolveThemeAll, resolveThemeItemAll, resolveThemeTypeAll


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

    @strawberryA.field(description="""last-change""")
    def lastchange(self) -> datetime:
        return self.lastchange

    # FK ################################################
    @strawberryA.field(description="""SemestersforSubject""")
    async def themes(self, info: strawberryA.types.Info) -> List['SubjectGQLModel']:
        result = await resolveSubjectsforProgram(AsyncSessionFromInfo(info), self.id)
        return result


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
        result = await resolveStudyProgramByID(AsyncSessionFromInfo(info), self.program_id)
        return result

    @strawberryA.field(description="""StudyLanguageID""")
    async def study_language(self, info: strawberryA.types.Info) -> 'StudyLanguageGQLModel':
        result = await resolveStudyLanguageByID(AsyncSessionFromInfo(info), self.language_id)
        return result

    @strawberryA.field(description="""SemestersforSubject""")
    async def themes(self, info: strawberryA.types.Info) -> List['SemesterGQLModel']:
        result = await resolveSemestersforSubject(AsyncSessionFromInfo(info), self.id)
        return result


### GQL SUBJECT UPDATE
@strawberryA.input(description="""Entity representing a subject update""")
class SubjectUpdateGQLModel:
    lastchange: datetime.datetime
    name: Optional[str] = None
    program_id: Optional[uuid.UUID] = None
    language_id: Optional[uuid.UUID] = None


### GQL SUBJECT EDITOR
from gql_granting.GraphResolvers import resolveUpdateSubject


@strawberryA.federation.type(keys=["id"], description="""Entity representing an editable subject""")
class SubjectEditorGQLModel:
    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveSubjectByID(session, id)
            result._type_definition = cls._type_definition
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result status of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    async def project(self, info: strawberryA.types.Info) -> SubjectGQLModel:
        async with withInfo(info) as session:
            result = await resolveSubjectByID(session, id)
            return result

    @strawberryA.field(description="""Updates the subject data""")
    async def update(self, info: strawberryA.types.Info, data: SubjectUpdateGQLModel) -> 'SubjectEditorGQLModel':
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdateSubject(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = SubjectEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result


### GQL SEMESTER UPDATE
@strawberryA.input(description="""Entity representing a semester update""")
class SemesterUpdateGQLModel:
    lastchange: datetime.datetime
    semester_number: Optional[int] = None
    credits: Optional[int] = None
    subject_id: Optional[uuid.UUID] = None
    classification_id: Optional[uuid.UUID] = None


### GQL SEMESTER EDITOR
from gql_granting.GraphResolvers import resolveRemoveTheme, resolveRemoveThemeItem, resolveRemoveThemeType, \
    resolveUpdateSemester, resolveInsertThemeItem, resolveInsertThemeType, resolveInsertTheme


@strawberryA.federation.type(keys=["id"], description="""Entity representing an editable semester""")
class SemesterEditorGQLModel:
    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveSemesterByID(session, id)
            result._type_definition = cls._type_definition
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result status of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    async def project(self, info: strawberryA.types.Info) -> 'SemesterGQLModel':
        async with withInfo(info) as session:
            result = await resolveSemesterByID(session, id)
            return result

    @strawberryA.field(description="""Updates the semester data""")
    async def update(self, info: strawberryA.types.Info, data: SemesterUpdateGQLModel) -> 'SemesterEditorGQLModel':
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdateSemester(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = SemesterEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result

    @strawberryA.field(description="""Create new Theme""")
    async def add_theme(self, info: strawberryA.types.Info, name: str, semester_id: uuid.UUID) -> 'StudyThemeGQLModel':
        async with withInfo(info) as session:
            result = await resolveInsertTheme(session, None, extraAttributes={'name': name, 'semester_id': self.id})
            return result

    @strawberryA.field(description="""Remove Theme""")
    async def remove_theme(self, info: strawberryA.types.Info, theme_id: uuid.UUID) -> str:
        async with withInfo(info) as session:
            result = await resolveRemoveTheme(session, self.id, theme_id)
            return result

    @strawberryA.filed(description="""Create new ThemeItem""")
    async def add_theme_item(self, info: strawberryA.types.Info, theme_id: uuid.UUID, type_id: uuid.UUID,
                             lessons: int) -> 'StudyThemeItemGQLModel':
        async with withInfo(info) as session:
            result = await resolveInsertThemeItem(session, None,
                                                  extraAttributes={'theme_id': theme_id, 'type_id': type_id,
                                                                   'lessons': lessons, 'semester_id': self.id})
            return result

    @strawberryA.field(description="""Remove ThemeItem""")
    async def remove_themeitem(self, info: strawberryA.types.Info, themeitem_id: uuid.UUID) -> str:
        async with withInfo(info) as session:
            result = await resolveRemoveTheme(session, self.id, themeitem_id)
            return result

    @strawberryA.filed(description="""Create new ThemeType""")
    async def add_theme_type(self, info: strawberryA.types.Info, name: str) -> 'ThemeTypeGQLModel':
        async with withInfo(info) as session:
            result = await resolveInsertThemeType(session, None, extraAttributes={'name': name, 'semester_id': self.id})
            return result

    @strawberryA.field(description="""Remove ThemeType""")
    async def remove_themetype(self, info: strawberryA.types.Info, themetype_id: uuid.UUID) -> str:
        async with withInfo(info) as session:
            result = await resolveRemoveThemeType(session, self.id, themetype_id)
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
        result = await resolveSubjectsforLanguage(AsyncSessionFromInfo(info), self.language_id)
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

    @strawberryA.field(description="""Returns the semester editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['SemesterEditorGQLModel', None]:
        return self

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
        result = await resolveThemesforSemester(AsyncSessionFromInfo(info), self.semester_id)
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
class StudyThemeGQLModel:  # Tema hodiny
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
        result = await resolveSemesterByID(AsyncSessionFromInfo(info), self.semester_id)
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
class ThemeTypeGQLModel:  # Prednaska/cvika/laborky
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

    # STUDY PROGRAM
    @strawberryA.field(description="""Finds study programs by their id""")
    async def study_program_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[StudyProgramGQLModel, None]:
        result = await resolveStudyProgramByID(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Returns list of study programs""")
    async def study_programs_list(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[StudyProgramGQLModel]:
        async with withInfo(info) as session:
            result = await resolveStudyProgramAll(session, skip, limit)
            return result

    # SUBJECT
    @strawberryA.field(description="""Finds subjects by their id""")
    async def subject_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[SubjectGQLModel, None]:
        result = await resolveSubjectByID(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Returns list of subjects""")
    async def subjects_list(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[SubjectGQLModel]:
        async with withInfo(info) as session:
            result = await resolveSubjectAll(session, skip, limit)
            return result

    # STUDY LANGUAGE

    @strawberryA.field(description="""Finds languages by their id""")
    async def study_language_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[StudyLanguageGQLModel, None]:
        result = await resolveStudyLanguageByID(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Returns list of languages""")
    async def languages_list(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[StudyLanguageGQLModel]:
        async with withInfo(info) as session:
            result = await resolveLanguageAll(session, skip, limit)
            return result

    # SEMESTER

    @strawberryA.field(description="""Finds semesters by their id""")
    async def semester_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[SemesterGQLModel, None]:
        result = await resolveSemesterByID(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Returns list of semesters""")
    async def semesters_list(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[SemesterGQLModel]:
        async with withInfo(info) as session:
            result = await resolveSemesterAll(session, skip, limit)
            return result

    # CLASSIFICATION

    @strawberryA.field(description="""Finds classifications by their id""")
    async def classification_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[ClassificationGQLModel, None]:
        result = await resolveClassificationByID(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Returns list of classifications""")
    async def classifications_list(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[ClassificationGQLModel]:
        async with withInfo(info) as session:
            result = await resolveClassificationAll(session, skip, limit)
            return result

    # STUDY THEME

    @strawberryA.field(description="""Finds study themes by their id""")
    async def study_theme_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[StudyThemeGQLModel, None]:
        result = await resolveStudyThemeByID(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Returns list of study themes""")
    async def themes_list(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[StudyThemeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveThemeAll(session, skip, limit)
            return result

    # STUDY THEME ITEM

    @strawberryA.field(description="""Finds study theme items by their id""")
    async def study_theme_item_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[StudyThemeItemGQLModel, None]:
        result = await resolveStudyThemeItemByID(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Returns list of theme items""")
    async def theme_items_list(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[
        StudyThemeItemGQLModel]:
        async with withInfo(info) as session:
            result = await resolveThemeItemAll(session, skip, limit)
            return result

    # STUDY THEME TYPE

    @strawberryA.field(description="""Finds study theme types by their id""")
    async def theme_type_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[ThemeTypeGQLModel, None]:
        result = await resolveThemeTypeByID(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Returns list of theme types""")
    async def theme_types_list(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[
        ThemeTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveThemeTypeAll(session, skip, limit)
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
