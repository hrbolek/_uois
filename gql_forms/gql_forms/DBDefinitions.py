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
import uuid

BaseModel = declarative_base()

def newUuidAsString():
    return f"{uuid.uuid1()}"


def UUIDColumn(name=None):
    if name is None:
        return Column(String, primary_key=True, unique=True, default=newUuidAsString)
    else:
        return Column(
            name, String, primary_key=True, unique=True, default=newUuidAsString
        )



# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################


class RequestModel(BaseModel):
    __tablename__ = "forms"

    id = UUIDColumn()
    name = Column(String)
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    status = Column(String)
    valid = Column(Boolean, default=True)
    sections = relationship("SectionModel", back_populates="request")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)


class SectionModel(BaseModel):
    __tablename__ = "formsections"

    # requestId = Column(ForeignKey("requests.id"), primary_key=True)
    # key is st sys structure name pr as id, fk follpw by id in lower letter

    id = UUIDColumn()
    name = Column(String)

    request_id = Column(ForeignKey("forms.id"), index=True)
    create_at = Column(DateTime)
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    order = Column(Integer)
    status = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)

    request = relationship("RequestModel", back_populates="sections")
    parts = relationship("PartModel", back_populates="section")


class PartModel(BaseModel):
    __tablename__ = "formparts"

    id = UUIDColumn()
    name = Column(String)

    create_at = Column(DateTime)
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    order = Column(Integer)

    section_id = Column(ForeignKey("formsections.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)

    section = relationship("SectionModel", back_populates="parts")
    items = relationship("ItemModel", back_populates="part")


class ItemModel(BaseModel):
    __tablename__ = "formitems"

    id = UUIDColumn()
    name = Column(String)

    create_at = Column(DateTime)
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    order = Column(Integer)

    value = Column(String)

    part_id = Column(ForeignKey("formparts.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = Column(ForeignKey("users.id"), index=True, nullable=True)

    part = relationship("PartModel", back_populates="items")


class UserModel(BaseModel):
    __tablename__ = "users"

    id = UUIDColumn()


#    request = relationship('RequestModel', back_populates='user')


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
