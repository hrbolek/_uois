from email.policy import default
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
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
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

def CreateUUIDFKey(allowCross=False):
    def UUIDFKey(ForeignKey=None, *, nullable=False, index=True):
        assert ForeignKey is not None, "ForeignKey is mandatory"
        return Column(
            ForeignKey, index=index, nullable=nullable
        )
    
    def UUIDFKeyDummy(ForeignKey=None, *, nullable=False, index=True):
        return Column(
            String, index=index, nullable=nullable
        )
    
    if allowCross:
        return UUIDFKey
    else:
        return UUIDFKeyDummy
    
UUIDFKey = CreateUUIDFKey()

# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

class SurveyModel(BaseModel):
    __tablename__ = "surveys"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    type_id = Column(ForeignKey("surveytypes.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(ForeignKey("users.id"), index=True, nullable=True)


class SurveyTypeModel(BaseModel):
    __tablename__ = "surveytypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)



class QuestionModel(BaseModel):
    __tablename__ = "surveyquestions"

    id = UUIDColumn()
    name = Column(String)  # kompletní znění otázky
    name_en = Column(String)
    order = Column(Integer)
    survey_id = Column(ForeignKey("surveys.id"), index=True)
    type_id = Column(ForeignKey("surveyquestiontypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)


class QuestionValueModel(BaseModel):
    __tablename__ = "surveyquestionvalues"

    id = UUIDColumn()
    name = Column(String)  # possible answer for selection (scale, or closed question)
    name_en = Column(String)
    order = Column(Integer)
    question_id = Column(ForeignKey("surveyquestions.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)


class QuestionTypeModel(BaseModel):
    __tablename__ = "surveyquestiontypes"
    id = UUIDColumn()
    name = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)


class AnswerModel(BaseModel):
    __tablename__ = "surveyanswers"

    id = UUIDColumn()
    value = Column(String)
    aswered = Column(Boolean)
    expired = Column(Boolean)
    user_id = UUIDFKey()#Column(ForeignKey("users.id"), index=True)
    question_id = Column(ForeignKey("surveyquestions.id"), primary_key=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)


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
