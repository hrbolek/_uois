import pytest

from gql_lessons.DBDefinitions import UserPlanModel, GroupPlanModel, PlannedLessonModel, FacilityPlanModel
from tests.shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata

from gql_lessons.GraphResolvers import resolveAddFacilitiesToPlan, resolveAddUsersToPlan, resolveAddGroupsToPlan
from gql_lessons.GraphResolvers import resolveRemoveFacilitiesFromPlan, resolveRemoveGroupsFromPlan, resolveRemoveUsersFromPlan

from sqlalchemy import select

@pytest.mark.asyncio
async def test_add_remove_users_to_plan():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    tables = get_demodata()

    table = tables['plan_lessons']
    row = table[0]
    planid = row['id']

    async with async_session_maker() as session:
        stmt = select(UserPlanModel)
        result = await session.execute(stmt)
        result = result.scalars().all()
        resultids = list(map(lambda item: item.user_id, result))

    await resolveRemoveUsersFromPlan(async_session_maker, planid, resultids)

    async with async_session_maker() as session:
        stmt = select(UserPlanModel)
        result = await session.execute(stmt)
        result = result.scalars().all()
        resultids = list(map(lambda item: item.user_id, result))

    assert len(resultids) == 0

    table = tables['users']
    userids = set(map(lambda item: item['id'], table))

    await resolveAddUsersToPlan(async_session_maker, planid, userids)

    async with async_session_maker() as session:
        stmt = select(UserPlanModel)
        result = await session.execute(stmt)
        result = result.scalars().all()
        resultids = list(map(lambda item: item.user_id, result))

    assert len(resultids) == len(userids)

@pytest.mark.asyncio
async def test_add_remove_groups_to_plan():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    tables = get_demodata()

    table = tables['plan_lessons']
    row = table[0]
    planid = row['id']

    async with async_session_maker() as session:
        stmt = select(GroupPlanModel)
        result = await session.execute(stmt)
        result = result.scalars().all()
        resultids = list(map(lambda item: item.group_id, result))

    await resolveRemoveGroupsFromPlan(async_session_maker, planid, resultids)

    async with async_session_maker() as session:
        stmt = select(GroupPlanModel)
        result = await session.execute(stmt)
        result = result.scalars().all()
        resultids = list(map(lambda item: item.group_id, result))

    assert len(resultids) == 0

    table = tables['groups']
    groupids = set(map(lambda item: item['id'], table))

    await resolveAddGroupsToPlan(async_session_maker, planid, groupids)

    async with async_session_maker() as session:
        stmt = select(GroupPlanModel)
        result = await session.execute(stmt)
        result = result.scalars().all()
        resultids = list(map(lambda item: item.group_id, result))
        
    assert len(resultids) == len(groupids)

@pytest.mark.asyncio
async def test_add_remove_facilities_to_plan():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    tables = get_demodata()

    table = tables['plan_lessons']
    row = table[0]
    planid = row['id']

    async with async_session_maker() as session:
        stmt = select(FacilityPlanModel)
        result = await session.execute(stmt)
        result = result.scalars().all()
        resultids = list(map(lambda item: item.facility_id, result))

    await resolveRemoveFacilitiesFromPlan(async_session_maker, planid, resultids)

    async with async_session_maker() as session:
        stmt = select(FacilityPlanModel)
        result = await session.execute(stmt)
        result = result.scalars().all()
        resultids = list(map(lambda item: item.facility_id, result))

    assert len(resultids) == 0

    table = tables['groups']
    facilityids = set(map(lambda item: item['id'], table))

    await resolveAddFacilitiesToPlan(async_session_maker, planid, facilityids)

    async with async_session_maker() as session:
        stmt = select(FacilityPlanModel)
        result = await session.execute(stmt)
        result = result.scalars().all()
        resultids = list(map(lambda item: item.facility_id, result))
        
    assert len(resultids) == len(facilityids)

from gql_lessons.GraphResolvers import resolveRemovePlan

@pytest.mark.asyncio
async def test_add_remove_plan():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    tables = get_demodata()

    table = tables['plan_lessons']
    row = table[0]
    planid = row['id']

    async with async_session_maker() as session:
        stmt = select(PlannedLessonModel)
        result = await session.execute(stmt)
        result = result.scalars().all()
        resultids = list(map(lambda item: item.id, result))
    rowCount = len(resultids)

    await resolveRemovePlan(async_session_maker, planid)

    async with async_session_maker() as session:
        stmt = select(PlannedLessonModel)
        result = await session.execute(stmt)
        result = result.scalars().all()
        resultids = list(map(lambda item: item.id, result))

    assert len(resultids) == rowCount - 1
