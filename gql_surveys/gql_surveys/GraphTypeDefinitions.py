from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
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
    print('obsolete function used AsyncSessionFromInfo, use withInfo context manager instead')
    return info.context['session']

from gql_surveys.GraphResolvers import resolveSurveyById, resolveQuestionById, resolveAnswerById, resolveUserById, resolveQuestionTypeById
from gql_surveys.GraphResolvers import resolveAnswersForQuestion,resolveAnswersForUser#, resolveQuestionsForType

@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel: 
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""List""")
    async def answers(self, info: strawberryA.types.Info) -> typing.List['AnswerGQLModel']:
        async with withInfo(info) as session:
            result = await resolveAnswersForUser(session,  self.id)
            return result

    @strawberryA.field(description="""List""")
    async def assignSurvey(self, info: strawberryA.types.Info, survey_id: strawberryA.ID) -> typing.List['AnswerGQLModel']: ###############
        async with withInfo(info) as session:
            result = await resolveAnswersForUser(session,  self.id)
            return result

@strawberryA.federation.type(keys=["id"], description="""Entity representing a relation between an user and a group""")
class QuestionTypeGQLModel: 
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveQuestionTypeById(session,  id)
            result._type_definition = cls._type_definition 
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Survey name""")
    def name(self) -> str:
        return self.name

from gql_surveys.GraphResolvers import resolveQuestionForSurvey
@strawberryA.federation.type(keys=["id"], description="""Entity representing a relation between an user and a group""")
class SurveyGQLModel:   

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveSurveyById(session,  id)
            result._type_definition = cls._type_definition 
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Survey name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""List""")
    async def questions(self, info: strawberryA.types.Info) -> typing.List['QuestionGQLModel']:
        async with withInfo(info) as session:
            result = await resolveQuestionForSurvey(session,  self.id)
            return result

#     @strawberryA.field(description="""List""")
#     async def editor(self, info: strawberryA.types.Info) -> 'SurveyEditorGQLModel':
#         return self

# @strawberryA.federation.type(keys=["id"], description="""Editor""") ###############
# class SurveyEditorGQLModel:
#     pass
    

@strawberryA.federation.type(keys=["id"], description="""Entity representing an access to information""")
class QuestionGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveQuestionById(session,  id)
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
    async def answers(self, info: strawberryA.types.Info) -> typing.List['AnswerGQLModel']:
        async with withInfo(info) as session:
            result = await resolveAnswersForQuestion(session,  self.id)
            return result

@strawberryA.federation.type(keys=["id"], description="""Entity representing an access to information""")
class AnswerGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveAnswerById(session,  id)
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

    @strawberryA.field(description="""is the survey still available?""") #mimo náš kontejner
    async def user(self) -> UserGQLModel:
        return UserGQLModel(self.user_id)

    @strawberryA.field(description="""is the survey still available?""") #v našem kontejneru
    async def question(self, info: strawberryA.types.Info) -> QuestionGQLModel:
        async with withInfo(info) as session:
            result = await resolveQuestionById(session,  self.question_id) 
            return result



from gql_surveys.DBFeeder import randomSurveyData

@strawberryA.type(description="""Type for query root""")
class Query:

    @strawberryA.field(description="""Finds a survey by its id""")
    async def survey_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[SurveyGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveSurveyById(session,  id)
            return result

    @strawberryA.field(description="""Question by id""")
    async def question_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[QuestionGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveQuestionById(session,  id)
            return result

    @strawberryA.field(description="""Question type by id""")
    async def question_type_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[QuestionTypeGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveQuestionTypeById(session,  id)
            return result

    @strawberryA.field(description="""Answer by id""")
    async def answer_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[AnswerGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveAnswerById(session,  id)
            return result
    
    @strawberryA.field(description="""Answer by id""")
    async def load_survey(self, info: strawberryA.types.Info) -> Union[SurveyGQLModel, None]:
        async with withInfo(info) as session:
            surveyID = await randomSurveyData(AsyncSessionFromInfo(info))
            result = await resolveSurveyById(session,  surveyID)
            return result

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))