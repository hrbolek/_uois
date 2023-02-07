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
from sqlalchemy.orm import declarative_base

from uoishelpers.uuid import UUIDColumn

BaseModel = declarative_base()

import uuid


def newUuidAsString():
    return f"{uuid.uuid1()}"


def UUIDColumn(name=None):
    if name is None:
        return Column(String, primary_key=True, unique=True, default=newUuidAsString)
    else:
        return Column(
            name, String, primary_key=True, unique=True, default=newUuidAsString
        )


class MembershipModel(BaseModel):
    """Spojuje User s Group jestlize User je clen Group
    Umoznuje udrzovat historii spojeni
    """

    __tablename__ = "memberships"

    id = UUIDColumn()
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    group_id = Column(ForeignKey("groups.id"), primary_key=True)

    startdate = Column(DateTime)
    enddate = Column(DateTime)
    valid = Column(Boolean, default=True)

    user = relationship("UserModel", back_populates="memberships")
    group = relationship("GroupModel", back_populates="memberships")


class UserModel(BaseModel):
    """Spravuje data spojena s uzivatelem"""

    __tablename__ = "users"

    id = UUIDColumn()
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    valid = Column(Boolean, default=True)
    startdate = Column(DateTime)
    enddate = Column(DateTime)

    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    memberships = relationship("MembershipModel", back_populates="user")
    roles = relationship("RoleModel", back_populates="user")


class GroupModel(BaseModel):
    """Spravuje data spojena se skupinou"""

    __tablename__ = "groups"

    id = UUIDColumn()
    name = Column(String)

    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    startDate = Column(DateTime)
    endDate = Column(DateTime)
    valid = Column(Boolean, default=True)

    grouptype_id = Column(ForeignKey("grouptypes.id"))
    grouptype = relationship("GroupTypeModel", back_populates="groups")

    mastergroup_id = Column(ForeignKey("groups.id"))

    memberships = relationship("MembershipModel", back_populates="group")
    roles = relationship("RoleModel", back_populates="group")


class GroupTypeModel(BaseModel):
    """Urcuje typ skupiny (fakulta, katedra, studijni skupina apod.)"""

    __tablename__ = "grouptypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    groups = relationship("GroupModel", back_populates="grouptype")


class RoleTypeModel(BaseModel):
    """Urcuje typ role (Vedouci katedry, dekan apod.)"""

    __tablename__ = "roletypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    roles = relationship("RoleModel", back_populates="roletype")


class RoleModel(BaseModel):
    """Spojuje uzivatele a skupinu, ve ktere uzivatel "hraje" roli"""

    __tablename__ = "roles"

    id = UUIDColumn()
    user_id = Column(ForeignKey("users.id"))
    group_id = Column(ForeignKey("groups.id"))
    roletype_id = Column(ForeignKey("roletypes.id"))

    startdate = Column(DateTime)
    enddate = Column(DateTime)
    valid = Column(Boolean)

    roletype = relationship("RoleTypeModel", back_populates="roles")
    user = relationship("UserModel", back_populates="roles")
    group = relationship("GroupModel", back_populates="roles")


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker"""
    asyncEngine = create_async_engine(connectionstring, pool_pre_ping=True)
    # pool_size=20, max_overflow=10, pool_recycle=60) #pool_pre_ping=True, pool_recycle=3600

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
