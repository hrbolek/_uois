import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_events")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from gql_events.DBDefinitions import BaseModel
from gql_events.DBDefinitions import EventModel, EventTypeModel, EventGroupModel
from gql_events.DBDefinitions import PresenceModel, PresenceTypeModel, InvitationTypeModel

from sqlalchemy.future import select

from shared import prepare_demodata, prepare_in_memory_sqllite, get_demodata


from gql_events.Dataloaders import createLoaders_3

@pytest.mark.asyncio
async def test_load_events():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    demodata = get_demodata()
    events = demodata['events']
    event0 = events[0]
    print(event0, flush=True)
    loaders = await createLoaders_3(async_session_maker)
    eventrow = await loaders.events.load(event0['id'])
    
    assert eventrow.id == event0['id']
    assert eventrow.name == event0['name']

@pytest.mark.asyncio
async def test_load_eventtypes():
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    demodata = get_demodata()
    events = demodata['eventtypes']
    event0 = events[0]
    print(event0, flush=True)
    loaders = await createLoaders_3(async_session_maker)
    eventrow = await loaders.eventtypes.load(event0['id'])
    
    assert eventrow.id == event0['id']
    assert eventrow.name == event0['name']
