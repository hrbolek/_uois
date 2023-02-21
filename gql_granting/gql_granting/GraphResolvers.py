from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, \
    createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_granting.DBDefinitions import BaseModel, StudyProgramModel, SubjectModel, StudyLanguageModel, SemesterModel, \
    ClassificationModel, StudyThemeModel, StudyThemeItemModel, ThemeTypeModel

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

# StudyProgramModel
resolveStudyProgramByID = createEntityByIdGetter(StudyProgramModel)
resolveSubjectsforProgram = create1NGetter(SubjectModel, foreignKeyName='program_id')
# Study->Subject 1/N

# SubjectModel
resolveSubjectByID = createEntityByIdGetter(SubjectModel)
resolveSemestersforSubject = create1NGetter(SemesterModel, foreignKeyName='subject_id')
# Subject -> Languguage 1/N
# Subject->Semester 1/N

# StudyLanguageModel
resolveStudyLanguageByID = createEntityByIdGetter(StudyLanguageModel)
resolveSubjectsforLanguage = create1NGetter(SubjectModel, foreignKeyName='language_id')

# SemesterModel
resolveSemesterByID = createEntityByIdGetter(SemesterModel)
resolveThemesforSemester = create1NGetter(StudyThemeModel, foreignKeyName='semester_id')
# Semester->Class 1/1
# Semester->StudyTheme 1/N

# ClassificationModel
resolveClassificationByID = createEntityByIdGetter(ClassificationModel)

# StudyThemeModel
resolveStudyThemeByID = createEntityByIdGetter(StudyThemeModel)

# StudyTheme->ThemeItem 1/N

# StudyThemeItemModel
resolveStudyThemeItemByID = createEntityByIdGetter(StudyThemeItemModel)
# ThemeItem->ThemeType 1/1

# ThemeTypeModel
resolveThemeTypeByID = createEntityByIdGetter(ThemeTypeModel)

###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

# resolveItemById = createEntityByIdGetter(EntityModel)
# resolveItemPage = createEntityGetter(EntityModel)

# ...
