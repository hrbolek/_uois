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

def getLoaders(info):
    return info.context['all']

from gql_surveys.GraphResolvers import (
    resolveSurveyById,
    resolveQuestionById,
    resolveAnswerById,
    resolveQuestionTypeById,
)
from gql_surveys.GraphResolvers import (
    resolveAnswersForQuestion,
    resolveAnswersForUser,
)  # , resolveQuestionsForType


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""List""")
    async def answers(
        self, info: strawberryA.types.Info
    ) -> typing.List["AnswerGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveAnswersForUser(session, self.id)
            return result

    @strawberryA.field(description="""List""")
    async def assignSurvey(
        self, info: strawberryA.types.Info, survey_id: strawberryA.ID
    ) -> typing.List["AnswerGQLModel"]:  ###############
        async with withInfo(info) as session:
            result = await resolveAnswersForUser(session, self.id)
            return result


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class QuestionTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).questiontypes
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Survey name""")
    def name(self) -> str:
        return self.name


from gql_surveys.GraphResolvers import resolveQuestionForSurvey
import datetime

@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class SurveyGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).surveys
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Survey name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""List""")
    async def questions(
        self, info: strawberryA.types.Info
    ) -> typing.List["QuestionGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveQuestionForSurvey(session, self.id)
            return result


#     @strawberryA.field(description="""List""")
#     async def editor(self, info: strawberryA.types.Info) -> 'SurveyEditorGQLModel':
#         return self

# @strawberryA.federation.type(keys=["id"], description="""Editor""") ###############
# class SurveyEditorGQLModel:
#     pass


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class QuestionGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).questions
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Question""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Order of questions""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""List""")
    async def answers(
        self, info: strawberryA.types.Info
    ) -> typing.List["AnswerGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveAnswersForQuestion(session, self.id)
            return result


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class AnswerGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).answers
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""answer""")
    def value(self) -> Union[str, None]:
        return self.value

    @strawberryA.field(description="""is the survey already answered?""")
    async def aswered(self) -> bool:
        return self.aswered

    @strawberryA.field(description="""is the survey still available?""")
    async def expired(self) -> bool:
        return self.expired

    @strawberryA.field(
        description="""is the survey still available?"""
    )  # mimo náš kontejner
    async def user(self) -> UserGQLModel:
        return await UserGQLModel.resolve_reference(self.user_id)

    @strawberryA.field(
        description="""is the survey still available?"""
    )  # v našem kontejneru
    async def question(self, info: strawberryA.types.Info) -> QuestionGQLModel:
        return await QuestionGQLModel.resolve_reference(info, self.question_id)


from gql_surveys.DBFeeder import randomSurveyData


@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Finds a survey by its id""")
    async def survey_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[SurveyGQLModel, None]:
        return await SurveyGQLModel.resolve_reference(info, id)

    @strawberryA.field(description="""Question by id""")
    async def question_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[QuestionGQLModel, None]:
        return await QuestionGQLModel.resolve_reference(info, id)

    @strawberryA.field(description="""Question type by id""")
    async def question_type_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[QuestionTypeGQLModel, None]:
        return await QuestionTypeGQLModel.resolve_reference(info, id)

    @strawberryA.field(description="""Answer by id""")
    async def answer_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[AnswerGQLModel, None]:
        print(id, flush=True)
        return await AnswerGQLModel.resolve_reference(info, id)

    @strawberryA.field(description="""Answer by id""")
    async def load_survey(
        self, info: strawberryA.types.Info
    ) -> Union[SurveyGQLModel, None]:
        async with withInfo(info) as session:
            surveyID = await randomSurveyData(AsyncSessionFromInfo(info))
            result = await resolveSurveyById(session, surveyID)
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
class SurveyInsertGQLModel:
    name: str
    name_en: Optional[str] = ""

    type_id: Optional[strawberryA.ID] = None
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class SurveyUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str] = None
    name_en: Optional[str] = None
    type_id: Optional[strawberryA.ID] = None
    
    
@strawberryA.type
class SurveyResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def survey(self, info: strawberryA.types.Info) -> Union[SurveyGQLModel, None]:
        result = await SurveyGQLModel.resolve_reference(info, self.id)
        return result


    
@strawberryA.federation.type(extend=True)
class Mutation:
    @strawberryA.mutation
    async def survey_insert(self, info: strawberryA.types.Info, survey: SurveyInsertGQLModel) -> SurveyResultGQLModel:
        loader = getLoaders(info).surveys
        row = await loader.insert(survey)
        result = SurveyResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation
    async def survey_update(self, info: strawberryA.types.Info, survey: SurveyUpdateGQLModel) -> SurveyResultGQLModel:
        loader = getLoaders(info).surveys
        row = await loader.update(survey)
        result = SurveyResultGQLModel()
        result.msg = "ok"
        result.id = survey.id
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
