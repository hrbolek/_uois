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

from uoishelpers.dataloaders import createIdLoader, createFkeyLoader


dbmodels = {
    "surveys": SurveyModel, 
    "surveytypes": SurveyTypeModel, 
    "questions": QuestionModel, 
    "questiontypes": QuestionTypeModel, 
    "questionvalues": QuestionValueModel, 
    "answers": AnswerModel
    
}

async def createLoaders(asyncSessionMaker, models=dbmodels):
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

from functools import cache