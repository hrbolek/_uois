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

from gql_projects.DBDefinitions import BaseModel

# přepsat na naše

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

from gql_projects.DBDefinitions import (
    ProjectModel,
    ProjectTypeModel,
    FinanceModel,
    FinanceTypeModel,
    MilestoneModel,
)

###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

# Project resolvers
resolveProjectById = createEntityByIdGetter(ProjectModel)
resolveProjectAll = createEntityGetter(ProjectModel)
resolveUpdateProject = createUpdateResolver(ProjectModel)
resolveInsertProject = createInsertResolver(ProjectModel)

resolveMilestonesForProject = create1NGetter(
    MilestoneModel, foreignKeyName="project_id"
)
resolveFinancesForProject = create1NGetter(
    FinanceModel,
    foreignKeyName="project_id",
    options=joinedload(FinanceModel.financeType),
)

# ProjectType resolvers
resolveProjectTypeById = createEntityByIdGetter(ProjectTypeModel)
resolveProjectTypeAll = createEntityGetter(ProjectTypeModel)
resolveUpdateProjectType = createUpdateResolver(ProjectTypeModel)
resolveInsertProjectType = createInsertResolver(ProjectTypeModel)

resolveProjectsForProjectType = create1NGetter(
    ProjectModel, foreignKeyName="projectType_id"
)

# Finance resolvers
resolveFinanceById = createEntityByIdGetter(FinanceModel)
resolveFinanceAll = createEntityGetter(FinanceModel)
resolveUpdateFinance = createUpdateResolver(FinanceModel)
resolveInsertFinance = createInsertResolver(FinanceModel)

# FinanceType resolvers
resolveFinanceTypeById = createEntityByIdGetter(FinanceTypeModel)
resolveFinanceTypeAll = createEntityGetter(FinanceTypeModel)
resolveUpdateFinanceType = createUpdateResolver(FinanceTypeModel)
resolveInsertFinanceType = createInsertResolver(FinanceTypeModel)

resolveFinancesForFinanceType = create1NGetter(
    FinanceModel, foreignKeyName="financeType_id"
)

# Milestone resolvers
resolveMilestoneById = createEntityByIdGetter(MilestoneModel)
resolveMilestoneAll = createEntityGetter(MilestoneModel)
resolveUpdateMilestone = createUpdateResolver(MilestoneModel)
resolveInsertMilestone = createInsertResolver(MilestoneModel)

# Group resolvers
resolveProjectsForGroup = create1NGetter(ProjectModel, foreignKeyName="group_id")
# ...
