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
resolveUpdateSubject = createUpdateResolver(SubjectModel)

# Subject -> Languguage 1/N
# Subject->Semester 1/N

# StudyLanguageModel
resolveStudyLanguageByID = createEntityByIdGetter(StudyLanguageModel)
resolveSubjectsforLanguage = create1NGetter(SubjectModel, foreignKeyName='language_id')

# SemesterModel
resolveSemesterByID = createEntityByIdGetter(SemesterModel)
resolveThemesforSemester = create1NGetter(StudyThemeModel, foreignKeyName='semester_id')
resolveUpdateSemester = createUpdateResolver(SemesterModel)
# Semester->Class 1/1
# Semester->StudyTheme 1/N

# ClassificationModel
resolveClassificationByID = createEntityByIdGetter(ClassificationModel)
resolveClassificationsforSemester = create1NGetter(ClassificationModel, foreignKeyName='classification_id')

# StudyThemeModel
resolveStudyThemeByID = createEntityByIdGetter(StudyThemeModel)
resolveUpdateTheme = createUpdateResolver(StudyThemeModel)
resolveInsertTheme = createInsertResolver(StudyThemeModel)

async def resolveRemoveTheme(session, subject_id, theme_id):
    stmt = delete(StudyThemeModel).where((StudyThemeModel.subject_id == subject_id) & (StudyThemeModel.id == theme_id))
    resultMsg = ""
    try:
        response = await session.execute(stmt)
        await session.commit()
        if (response.rowcount == 1):
            resultMsg = "ok"
        else:
            resultMsg = "fail"
    except:
        resultMsg = "error"

    return resultMsg


# StudyTheme->ThemeItem 1/N

# StudyThemeItemModel
resolveStudyThemeItemByID = createEntityByIdGetter(StudyThemeItemModel)
resolveUpdateThemeItem = createUpdateResolver(StudyThemeItemModel)
resolveInsertThemeItem = createInsertResolver(StudyThemeItemModel)

async def resolveRemoveThemeItem(session, subject_id, theme_item_id):
    stmt = delete(StudyThemeModel).where(
        (StudyThemeModel.subject_id == subject_id) & (StudyThemeModel.id == theme_item_id))
    resultMsg = ""
    try:
        response = await session.execute(stmt)
        await session.commit()
        if (response.rowcount == 1):
            resultMsg = "ok"
        else:
            resultMsg = "fail"
    except:
        resultMsg = "error"

    return resultMsg


# ThemeItem->ThemeType 1/1

# ThemeTypeModel
resolveThemeTypeByID = createEntityByIdGetter(ThemeTypeModel)
resolveUpdateThemeType = createUpdateResolver(ThemeTypeModel)
resolveInsertThemeType = createInsertResolver(ThemeTypeModel)
async def resolveRemoveThemeType(session, subject_id, theme_type_id):
    stmt = delete(StudyThemeModel).where(
        (StudyThemeModel.subject_id == subject_id) & (StudyThemeModel.id == theme_type_id))
    resultMsg = ""
    try:
        response = await session.execute(stmt)
        await session.commit()
        if (response.rowcount == 1):
            resultMsg = "ok"
        else:
            resultMsg = "fail"
    except:
        resultMsg = "error"

    return resultMsg

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
