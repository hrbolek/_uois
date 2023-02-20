from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import (
    create1NGetter,
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
    createUpdateResolver,
)
from uoishelpers.resolvers import putSingleEntityToDb

from gql_surveys.DBDefinitions import BaseModel

from gql_surveys.DBDefinitions import (
    SurveyModel,
    QuestionModel,
    AnswerModel,
    QuestionTypeModel,
)

# users
#resolveUserPaged = createEntityGetter(UserModel)
#resolveUserById = createEntityByIdGetter(UserModel)
#resolveUserSurvey = createInsertResolver(UserModel)

resolveAnswersForUser = create1NGetter(AnswerModel, foreignKeyName="user_id")

# surveys
resolveSurveyPaged = createEntityGetter(SurveyModel)
resolveSurveyById = createEntityByIdGetter(SurveyModel)
resolveInsertSurvey = createInsertResolver(SurveyModel)

resolveQuestionForSurvey = create1NGetter(QuestionModel, foreignKeyName="survey_id")

# questions
resolveQuestionPaged = createEntityGetter(QuestionModel)
resolveQuestionById = createEntityByIdGetter(QuestionModel)
resolveInsertQuestion = createInsertResolver(QuestionModel)

resolveAnswersForQuestion = create1NGetter(AnswerModel, foreignKeyName="question_id")


# question types
resolveQuestionTypePaged = createEntityGetter(QuestionTypeModel)
resolveQuestionTypeById = createEntityByIdGetter(QuestionTypeModel)
resolveInsertQuestionType = createInsertResolver(QuestionTypeModel)


# answers
resolveAnswerPaged = createEntityGetter(AnswerModel)
resolveAnswerById = createEntityByIdGetter(AnswerModel)
resolveAnswerQuestion = createInsertResolver(AnswerModel)
