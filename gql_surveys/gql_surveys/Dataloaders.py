from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from functools import cache

from gql_surveys.DBDefinitions import (
    SurveyModel, SurveyTypeModel, QuestionModel, QuestionTypeModel, QuestionValueModel, AnswerModel)

async def createLoaders_3(asyncSessionMaker):
    class Loaders:
        @property
        @cache
        def surveys(self):
            return createIdLoader(asyncSessionMaker, SurveyModel)

        @property
        @cache
        def surveytypes(self):
            return createIdLoader(asyncSessionMaker, SurveyTypeModel)

        @property
        @cache
        def questions(self):
            return createIdLoader(asyncSessionMaker, QuestionModel)

        @property
        @cache
        def questiontypes(self):
            return createIdLoader(asyncSessionMaker, QuestionTypeModel)

        @property
        @cache
        def questionvalues(self):
            return createIdLoader(asyncSessionMaker, QuestionValueModel)

        @property
        @cache
        def answers(self):
            return createIdLoader(asyncSessionMaker, AnswerModel)

    
    return Loaders()