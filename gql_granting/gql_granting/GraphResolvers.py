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


###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

from gql_granting.DBDefinitions import (
    BaseModel,
    ProgramFormTypeModel,
    ProgramGroupModel,
    ProgramLanguageTypeModel,
    ProgramLevelTypeModel,
    ProgramModel,
    ProgramTitleTypeModel,
)
from gql_granting.DBDefinitions import (
    BaseModel,
    SubjectModel,
    SemesterModel,
    ClassificationTypeModel,
    LessonModel,
    LessonTypeModel,
    TopicModel,
)
from gql_granting.DBDefinitions import ProgramGroupModel

###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

# resolveItemById = createEntityByIdGetter(EntityModel)
# resolveItemPage = createEntityGetter(EntityModel)

resolveGroupsForProgram_ = create1NGetter(
    ProgramGroupModel, foreignKeyName="program_id"
)
resolveProgramForGroup_ = create1NGetter(ProgramGroupModel, foreignKeyName="group_id")


async def resolveProgramForGroup(session, id):
    links = await resolveProgramForGroup_(session, id)
    links = list(links)
    if len(links) == 0:
        result = None
    else:
        link = links[0]
        result = await resolveProgramById(session, link.program_id)
    return result


async def resolveGroupIdsForProgram(session, id):
    links = await resolveGroupsForProgram_(session, id)
    links = list(links)
    result = list(map(lambda item: item.group_id, links))
    return result


resolveProgramById = createEntityByIdGetter(ProgramModel)
resolveProgramPage = createEntityGetter(ProgramModel)

programSelect = select(ProgramModel)
subjectSelect = select(SubjectModel)
classificationTypeSelect = select(ClassificationTypeModel)

resolveLanguageTypeById = createEntityByIdGetter(ProgramLanguageTypeModel)
resolveLevelTypeById = createEntityByIdGetter(ProgramLevelTypeModel)
resolveFormTypeById = createEntityByIdGetter(ProgramFormTypeModel)
resolveTitleTypeById = createEntityByIdGetter(ProgramTitleTypeModel)

resolveSubjectById = createEntityByIdGetter(SubjectModel)
resolveSubjectPage = createEntityGetter(SubjectModel)
resolveSubjectsForProgram = create1NGetter(SubjectModel, foreignKeyName="program_id")

resolveSemesterById = createEntityByIdGetter(SemesterModel)
resolveSemesterPage = createEntityGetter(SemesterModel)
resolveSemestersForSubject = create1NGetter(SemesterModel, foreignKeyName="subject_id")

resolveClassificationTypeById = createEntityByIdGetter(ClassificationTypeModel)

resolveTopicById = createEntityByIdGetter(TopicModel)
resolveTopicPage = createEntityGetter(TopicModel)
resolveTopicsForSemester = create1NGetter(TopicModel, foreignKeyName="semester_id")

resolveLessonById = createEntityByIdGetter(LessonModel)
resolveLessonPage = createEntityGetter(LessonModel)
resolveLessonsForTopics = create1NGetter(LessonModel, foreignKeyName="topic_id")

resolveLessonTypeById = createEntityByIdGetter(LessonTypeModel)


async def resolveJSONForProgram(session, id):
    """Just to speed up reading the complex structure"""
    return {
        "id": id,
        "subjects": [
            {
                "id": "unknown",
                "name": "TODO",
                "semesters": [
                    {
                        "id": "unknown",
                        "order": 1,
                        "classificationtype_id": "unknown",
                        "topics": [
                            {
                                "id": "unknown",
                                "order": 1,
                                "name": "uvod",
                                "lessons": [
                                    {
                                        "type_id": "unknown",
                                        "name": "Prednaska",
                                        "abbr": "P",
                                        "count": 2,
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
        "groupids": ["unknown"],
    }
    pass


# ...
