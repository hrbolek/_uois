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

from gql_lessons.DBDefinitions import (
    BaseModel,
    PlannedLessonModel,
    UserPlanModel,
    GroupPlanModel,
    FacilityPlanModel,
)

# from gql_lessons.DBDefinitions import UnavailabilityPL, UnavailabilityUser, UnavailabilityFacility
# from gql_lessons.DBDefinitions import FacilityModel

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################


###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

resolvePlannedLessonPage = createEntityGetter(
    PlannedLessonModel
)  # fuction. return a list
resolvePlannedLessonById = createEntityByIdGetter(PlannedLessonModel)  # single row .
resolvePlannedLessonByTopic = create1NGetter(
    PlannedLessonModel, foreignKeyName="topic_id"
)
resolvePlannedLessonBySemester = create1NGetter(
    PlannedLessonModel, foreignKeyName="semester_id"
)
resolvePlannedLessonByEvent = create1NGetter(
    PlannedLessonModel, foreignKeyName="event_id"
)
resolvePlannedLessonsByLink = create1NGetter(
    PlannedLessonModel, foreignKeyName="linkedlesson_id"
)

# intermediate data resolver
resolveUserLinksForPlannedLesson = create1NGetter(
    UserPlanModel, foreignKeyName="plannedlesson_id"
)  #
resolveGroupLinksForPlannedLesson = create1NGetter(
    GroupPlanModel, foreignKeyName="plannedlesson_id"
)
resolveFacilityLinksForPlannedLesson = create1NGetter(
    FacilityPlanModel, foreignKeyName="plannedlesson_id"
)
# resolveEventLinksForPlannedLesson = create1NGetter(Eve)

# unavailable Plan lesson resolver
# resolveUnavailabilityPLById = createEntityByIdGetter(UnavailabilityPL)
# resolveUnavailabilityPLAll = createEntityGetter(UnavailabilityPL)
# resolverUpdateUnavailabilityPL = createUpdateResolver(UnavailabilityPL)
# resolveInsertUnavailabilityPL = createInsertResolver(UnavailabilityPL)

# unavailable User resolver
# resolveUnavailabilityUserById = createEntityByIdGetter(UnavailabilityUser)
# resolveUnavailabilityUserAll = createEntityGetter(UnavailabilityUser)
# resolverUpdateUnavailabilityUser = createUpdateResolver(UnavailabilityUser)
# resolveInsertUnavailabilityUser = createInsertResolver(UnavailabilityUser)

# unavailable Facility resolver
# resolveUnavailabilityFacilityById = createEntityByIdGetter(UnavailabilityFacility)
# resolveUnavailabilityFacilityAll = createEntityGetter(UnavailabilityFacility)
# resolverUpdateUnavailabilityFacility = createUpdateResolver(UnavailabilityFacility)
# resolveInsertUnavailabilityFacility = createInsertResolver(UnavailabilityFacility)

from sqlalchemy import delete, insert

async def resolveRemoveUsersFromPlan(asyncSessionMaker, plan_id, usersids):
    deleteStmt = (delete(UserPlanModel)
        .where(UserPlanModel.planlesson_id==plan_id)
        .where(UserPlanModel.user_id.in_(usersids)))
    async with asyncSessionMaker() as session:
        await session.execute(deleteStmt)
        await session.commit()

async def resolveAddUsersToPlan(asyncSessionMaker, plan_id, usersids):
    async with asyncSessionMaker() as session:
        await session.execute(insert(UserPlanModel), [{"plan_id": plan_id, "user_id": user_id} for user_id in usersids])
        await session.commit()

async def resolveRemoveGroupsFromPlan(asyncSessionMaker, plan_id, groupids):
    deleteStmt = (delete(GroupPlanModel)
        .where(GroupPlanModel.planlesson_id==plan_id)
        .where(GroupPlanModel.group_id.in_(groupids)))
    async with asyncSessionMaker() as session:
        await session.execute(deleteStmt)
        await session.commit()

async def resolveAddGroupsToPlan(asyncSessionMaker, plan_id, groupids):
    async with asyncSessionMaker() as session:
        await session.execute(insert(GroupPlanModel), [{"plan_id": plan_id, "group_id": group_id} for group_id in groupids])
        await session.commit()

async def resolveRemoveFacilitiesFromPlan(asyncSessionMaker, plan_id, facilityids):
    deleteStmt = (delete(FacilityPlanModel)
        .where(FacilityPlanModel.planlesson_id==plan_id)
        .where(FacilityPlanModel.facility_id.in_(facilityids)))
    async with asyncSessionMaker() as session:
        await session.execute(deleteStmt)
        await session.commit()

async def resolveAddFacilitiesToPlan(asyncSessionMaker, plan_id, facilityids):
    async with asyncSessionMaker() as session:
        await session.execute(insert(FacilityPlanModel), [{"plan_id": plan_id, "facility_id": facility_id} for facility_id in facilityids])
        await session.commit()

async def resolveRemovePlan(asyncSessionMaker, plan_id):
    deleteAStmt = delete(UserPlanModel).where(UserPlanModel.planlesson_id==plan_id)
    deleteBStmt = delete(GroupPlanModel).where(GroupPlanModel.planlesson_id==plan_id)
    deleteCStmt = delete(FacilityPlanModel).where(FacilityPlanModel.planlesson_id==plan_id)
    deleteDStmt = delete(PlannedLessonModel).where(PlannedLessonModel.id==plan_id)
    async with asyncSessionMaker() as session:
        await session.execute(deleteAStmt)
        await session.execute(deleteBStmt)
        await session.execute(deleteCStmt)
        await session.execute(deleteDStmt)
        await session.commit()
