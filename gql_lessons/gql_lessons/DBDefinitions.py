import sqlalchemy
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def UUIDColumn(name=None):
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    
#id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################


class PlannedLessonModel(BaseModel):
    """Defines a lesson which is going to be planned in timetable
    """

    __tablename__ = 'planned_lessons'
    
    id = UUIDColumn()
    

class UnavailabilityPL(BaseModel):
    """Defines a lesson which is unavailable in timetable
    """
    __tablename__ = 'unavailable_planned_lessons'

    id=UUIDColumn()
    plannedlesson_id=Column(ForeignKey('planned_lessons.id'))
    startDate=Column(DateTime)
    endDate=Column(DateTime)


class UserModel(BaseModel):
    """Defines user in the lession
    """

    __tablename__ = 'users'

    id = UUIDColumn()
    

class UserPlan(BaseModel):
    __tablename__ = 'users_plans'

    id=UUIDColumn()
    user_id=Column(ForeignKey('users.id'))
    plannedlesson_id=Column(ForeignKey('planned_lessons.id'))

class UnavailabilityUser(BaseModel):
    __tablename__ = 'unavailable_users'

    id=UUIDColumn()
    user_id=Column(ForeignKey('users.id'))
    startDate=Column(DateTime)
    endDate=Column(DateTime)

class GroupModel(BaseModel):
    __tablename__ = 'groups'

    id=UUIDColumn()

class GroupPlan(BaseModel):
    __tablename__ = 'groups_plans'    

    id=UUIDColumn()
    group_id=Column(ForeignKey('groups.id'))
    plannedlession_id=Column(ForeignKey('planned_lessons.id'))

class Event(BaseModel):
    __tablename__ = 'events'

    id=UUIDColumn()

class EventPlan(BaseModel):
    __tablename__ = 'events_plans'

    id = UUIDColumn()
    event_id=Column(ForeignKey('events.id'))
    plannedlession_id=Column(ForeignKey('planned_lessons.id'))

class Facility(BaseModel):
    __tablename__ = 'facilities'

    id=UUIDColumn()

class FacilityPlan(BaseModel):
    __tablename__ = 'facilities_plans'

    id=UUIDColumn()
    facility_id=Column(ForeignKey('facilities.id'))
    plannedlession_id=Column(ForeignKey('planned_lessons.id'))

class UnavailabilityFacility(BaseModel):
    __tablename__ = 'unavailable_facilities'

    id=UUIDColumn()
    facility_id=Column(ForeignKey('facilities.id'))
    startDate=Column(DateTime)
    endDate=Column(DateTime)


###########################################################
 


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker """
    asyncEngine = create_async_engine(connectionstring) 

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print('BaseModel.metadata.drop_all finished')
        if makeUp:
            await conn.run_sync(BaseModel.metadata.create_all)    
            print('BaseModel.metadata.create_all finished')

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker

import os
def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
       Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database =  os.environ.get("POSTGRES_DB", "data")
    hostWithPort =  os.environ.get("POSTGRES_HOST", "postgres:5432")
    
    driver = "postgresql+asyncpg" #"postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring