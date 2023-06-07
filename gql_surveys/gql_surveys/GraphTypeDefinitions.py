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
class SurveyTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).surveytypes
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

    @strawberryA.field(description="""time stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Question""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Order of questions""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""List of answers""")
    async def answers(
        self, info: strawberryA.types.Info
    ) -> typing.List["AnswerGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveAnswersForQuestion(session, self.id)
            return result

    @strawberryA.field(description="""Survey which owns this question""")
    async def survey(
        self, info: strawberryA.types.Info
    ) -> typing.Union["SurveyGQLModel", None]:
        result = await SurveyGQLModel.resolve_reference(info, self.survey_id)
        return result

    @strawberryA.field(description="""Type of question""")
    async def type(
        self, info: strawberryA.types.Info
    ) -> typing.Union["QuestionTypeGQLModel", None]:
        result = await QuestionTypeGQLModel.resolve_reference(info, self.type_id)
        return result

    @strawberryA.field(description="""List of values for closed or similar type questions""")
    async def values(
        self, info: strawberryA.types.Info
    ) -> typing.List["QuestionValueGQLModel"]:
        loader = getLoaders(info).questionvalues
        result = await loader.filter_by(question_id=self.id)
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

    @strawberryA.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""answer content / value""")
    def value(self) -> Union[str, None]:
        return self.value

    @strawberryA.field(description="""is the survey already answered?""")
    async def aswered(self) -> Union[bool, None]:
        return self.aswered

    @strawberryA.field(description="""is the survey still available?""")
    async def expired(self) -> Union[bool, None]:
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

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an access to information"""
)
class QuestionValueGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).questionvalues
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
    
    @strawberryA.field(description="""Name aka, value of answer""")
    def name(self) -> Union[str, None]:
        return self.name
    
    @strawberryA.field(description="""English name aka, value of answer""")
    def name_en(self) -> Union[str, None]:
        return self.name_en

    @strawberryA.field(description="""order of value""")
    def order(self) -> int:
        return self.order

    @strawberryA.field(description="""Question which has this possible answer""")
    async def question(self, info: strawberryA.types.Info) -> Union[QuestionGQLModel, None]:
        result = await QuestionGQLModel.resolve_reference(info, self.question_id)
        return result

from gql_surveys.DBFeeder import randomSurveyData

@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Page of survey types""")
    async def survey_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[SurveyTypeGQLModel]:
        loader = getLoaders(info).surveytypes
        result = await loader.page(skip, limit)
        return result
    
    @strawberryA.field(description="""Finds a survey type by its id""")
    async def survey_type_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[SurveyTypeGQLModel, None]:
        return await SurveyTypeGQLModel.resolve_reference(info, id)
    
    @strawberryA.field(description="""Finds a survey by its id""")
    async def survey_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[SurveyGQLModel, None]:
        return await SurveyGQLModel.resolve_reference(info, id)

    @strawberryA.field(description="""Page of surveys""")
    async def survey_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[SurveyGQLModel]:
        loader = getLoaders(info).surveys
        result = await loader.page(skip, limit)
        return result
    
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

    @strawberryA.field(description="""Question type by id""")
    async def question_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[QuestionTypeGQLModel]:
        loader = getLoaders(info).questiontypes
        result = await loader.page(skip, limit)
        return result

    @strawberryA.field(description="""Answer by id""")
    async def answer_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[AnswerGQLModel, None]:
        print(id, flush=True)
        return await AnswerGQLModel.resolve_reference(info, id)
    

    @strawberryA.field(description="""Answer by user""")
    async def answers_by_user(
        self, info: strawberryA.types.Info, user_id: strawberryA.ID
    ) -> Union[AnswerGQLModel, None]:
        loader = getLoaders(info).answers
        result = await loader.filter_by(user_id=user_id)
        return result  

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

    @strawberryA.field(description="""Result of survey operation""")
    async def survey(self, info: strawberryA.types.Info) -> Union[SurveyGQLModel, None]:
        result = await SurveyGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class AnswerUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    value: Optional[str] = None
    aswered: Optional[bool] = None   
    expired: Optional[bool] = None   
    
@strawberryA.type
class AnswerResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of answer operation""")
    async def answer(self, info: strawberryA.types.Info) -> Union[AnswerGQLModel, None]:
        result = await AnswerGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class QuestionInsertGQLModel:
    name: str
    survey_id: strawberryA.ID
    name_en: Optional[str] = ""
    type_id: Optional[strawberryA.ID] = None
    order: Optional[int] = 1
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class QuestionUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str] = None
    name_en: Optional[str] = None
    type_id: Optional[strawberryA.ID] = None
    order: Optional[int] = None

@strawberryA.type
class QuestionResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of question operation""")
    async def question(self, info: strawberryA.types.Info) -> Union[QuestionGQLModel, None]:
        result = await QuestionGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.input
class QuestionValueInsertGQLModel:
    question_id: strawberryA.ID
    name: str
    name_en: Optional[str] = ""   
    order: Optional[int] = 1
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class QuestionValueUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str] = None
    name_en: Optional[str] = None
    order: Optional[int] = None

@strawberryA.type
class QuestionValueResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of question operation""")
    async def question(self, info: strawberryA.types.Info) -> Union[QuestionValueGQLModel, None]:
        result = await QuestionValueGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.type
class Mutation:
    @strawberryA.mutation(description="""Creates new question value for closed question""")
    async def question_value_insert(self, info: strawberryA.types.Info, question_value: QuestionValueInsertGQLModel) -> QuestionValueResultGQLModel:
        loader = getLoaders(info).questionvalues
        row = await loader.insert(question_value)
        result = QuestionValueResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="""Updates question value / possible answer""")
    async def question_value_update(self, info: strawberryA.types.Info, question_value: QuestionValueUpdateGQLModel) -> QuestionValueResultGQLModel:
        loader = getLoaders(info).questionvalues
        row = await loader.update(question_value)
        result = QuestionValueResultGQLModel()
        result.msg = "ok"
        result.id = question_value.id
        if row is None:
            result.msg = "fail"           
        return result

    @strawberryA.mutation(description="""Updates question value / possible answer""")
    async def question_value_delete(self, info: strawberryA.types.Info, question_value_id: strawberryA.ID) -> QuestionResultGQLModel:
        loader = getLoaders(info).questionvalues
        row = await loader.load(question_value_id)
        await loader.delete(question_value_id)
        result = QuestionResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        if row is None:
            result.msg = "fail"           
        return result

    @strawberryA.mutation(description="""Creates new question in the survey""")
    async def question_insert(self, info: strawberryA.types.Info, question: QuestionInsertGQLModel) -> QuestionResultGQLModel:
        loader = getLoaders(info).questions
        row = await loader.insert(question)
        result = QuestionResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="""Updates question""")
    async def question_update(self, info: strawberryA.types.Info, question: QuestionUpdateGQLModel) -> QuestionResultGQLModel:
        loader = getLoaders(info).questions
        row = await loader.update(question)
        result = QuestionResultGQLModel()
        result.msg = "ok"
        result.id = question.id
        if row is None:
            result.msg = "fail"           
        return result

    @strawberryA.mutation(description="""Creates new survey""")
    async def survey_insert(self, info: strawberryA.types.Info, survey: SurveyInsertGQLModel) -> SurveyResultGQLModel:
        loader = getLoaders(info).surveys
        row = await loader.insert(survey)
        result = SurveyResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="""Updates the survey""")
    async def survey_update(self, info: strawberryA.types.Info, survey: SurveyUpdateGQLModel) -> SurveyResultGQLModel:
        loader = getLoaders(info).surveys
        row = await loader.update(survey)
        result = SurveyResultGQLModel()
        result.msg = "ok"
        result.id = survey.id
        if row is None:
            result.msg = "fail"           
        return result

    @strawberryA.mutation(description="""Assigns the survey to the user. For all questions in the survey are created empty answers for the user.""")
    async def survey_assing_to(self, info: strawberryA.types.Info, survey_id: strawberryA.ID, user_id: strawberryA.ID) -> SurveyResultGQLModel:
        loader = getLoaders(info).questions
        questions = await loader.filter_by(survey_id=survey_id)
        loader = getLoaders(info).answers
        for q in questions:
            exists = await loader.filter_by(question_id=q.id, user_id=user_id)
            if next(exists, None) is None:
                #user has not this particular question
                rowa = await loader.insert(None, {"question_id": q.id, "user_id": user_id})
        result = SurveyResultGQLModel()
        result.msg = "ok"
        result.id = survey_id
            
        return result

    @strawberryA.mutation(description="""Allows update a question.""")
    async def answer_update(self, info: strawberryA.types.Info, answer: AnswerUpdateGQLModel) -> AnswerResultGQLModel:
        loader = getLoaders(info).answers
        row = await loader.update(answer)
        result = AnswerResultGQLModel()
        result.msg = "ok"
        result.id = answer.id
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
