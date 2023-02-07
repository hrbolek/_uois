from unicodedata import name
import sqlalchemy
import datetime

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    DateTime,
    ForeignKey,
    Sequence,
    Table,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()
###


def UUIDColumn(name=None):
    if name is None:
        return Column(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sqlalchemy.text("gen_random_uuid()"),
            unique=True,
        )
    else:
        return Column(
            name,
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sqlalchemy.text("gen_random_uuid()"),
            unique=True,
        )


# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#


""" class MembershipModel(BaseModel):
    """


class FacilityModel(BaseModel):
    """Spravuje data spojena s objektem daneho typu"""

    __tablename__ = "facilities"

    id = UUIDColumn()
    name = Column(String)
    label = Column(String)
    address = Column(String)
    valid = Column(Boolean, default=True)
    startdate = Column(DateTime)
    enddate = Column(DateTime)
    capacity = Column(Integer)
    geometry = Column(String)
    geolocation = Column(String)

    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    group_id = Column(ForeignKey("groups.id"), primary_key=True)
    facilitytype_id = Column(ForeignKey("facilitytypes.id"))
    master_facility_id = Column(ForeignKey("facilities.id"), index=True, nullable=True)


class FacilityTypeModel(BaseModel):
    """Urcuje typ objektu (areal, budova, patro, mistnost)"""

    __tablename__ = "facilitytypes"
    id = UUIDColumn()
    name = Column(String)

    facilities = relationship("FacilityModel", back_populates="facilitytype")


class EventFacilityModel(BaseModel):
    __tablename__ = "facilities_events"

    id = UUIDColumn()
    event_id = Column(ForeignKey("events.id"))
    facility_id = Column(ForeignKey("facilities.id"))
    state_id = Column(ForeignKey("facilityeventstatetypes.id"))


class EventFacilityStateType(BaseModel):
    __tablename__ = "facilityeventstatetypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    # rozvrh, naplánováno, žádost, schváleno, zrušeno, ...
    # planned, requested, accepted, canceled, priority0, priority1, ...


class EventModel(BaseModel):
    __tablename__ = "events"

    id = UUIDColumn()


class GroupModel(BaseModel):
    """Spravuje data spojena se skupinou"""

    __tablename__ = "groups"

    id = UUIDColumn()


class UserModel(BaseModel):
    """Spravuje data spojena s uzivatelem"""

    __tablename__ = "users"

    id = UUIDColumn()


# name = Column(String)
# surname = Column(String)

# externalId = Column(BigInteger, index=True)


###########################################################################################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker"""
    asyncEngine = create_async_engine(connectionstring)

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print("BaseModel.metadata.drop_all finished")
        if makeUp:
            try:
                await conn.run_sync(BaseModel.metadata.create_all)
                print("BaseModel.metadata.create_all finished")
            except sqlalchemy.exc.NoReferencedTableError as e:
                print(e)
                print("Unable automaticaly create tables")
                return None

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
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "postgres:5432")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring
