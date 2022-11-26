from typing import List, Union
import typing
import strawberry as strawberryA
import uuid

def AsyncSessionFromInfo(info):
    return info.context['session']

from gql_survey.GraphResolvers import resolveSurveyById, resolveQuestionById, resolveAnswerById, resolveUserById, resolveQuestionTypeById

@strawberryA.federation.type(keys=["id"], description="""Entity representing a relation between an user and a group""")
class UserGQLModel: 
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

@strawberryA.federation.type(keys=["id"], description="""Entity representing a relation between an user and a group""")
class QuestionTypeGQLModel: 
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveQuestionTypeById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition 
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Survey name""")
    def name(self) -> str:
        return self.name

@strawberryA.federation.type(keys=["id"], description="""Entity representing a relation between an user and a group""")
class SurveyGQLModel:   

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveSurveyById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition 
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Survey name""")
    def name(self) -> str:
        return self.name

@strawberryA.federation.type(keys=["id"], description="""Entity representing an access to information""")
class QuestionGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveQuestionById(AsyncSessionFromInfo(info), id)
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

@strawberryA.federation.type(keys=["id"], description="""Entity representing an access to information""")
class AnswerGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveAnswerById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""answer""")
    def value(self) -> str:
        return self.value

    @strawberryA.field(description="""is the survey already answered?""")
    async def answered(self) -> bool:
        return self.answered

    @strawberryA.field(description="""is the survey still available?""")
    async def expired(self) -> bool:
        return self.expired



@strawberryA.type(description="""Type for query root""")
class Query:

    @strawberryA.field(description="""User by id""")
    async def answer_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[UserGQLModel, None]:
        result = await resolveUserById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds an survey by its id""")
    async def survey_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[SurveyGQLModel, None]:
        result = await resolveSurveyById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Question by id""")
    async def question_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[QuestionGQLModel, None]:
        result = await resolveQuestionById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Question type by id""")
    async def answer_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[QuestionTypeGQLModel, None]:
        result = await resolveQuestionTypeById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Answer by id""")
    async def answer_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[AnswerGQLModel, None]:
        result = await resolveAnswerById(AsyncSessionFromInfo(info), id)
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