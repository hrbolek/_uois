from email.policy import default
import sqlalchemy
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def UUIDColumn(name=None):
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"),unique=True)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"),unique=True)

#id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)
class UserModel(BaseModel):
    __tablename__ = 'users'

    id = UUIDColumn() 

class SurveyModel(BaseModel):
    __tablename__ = 'surveys'

    id = UUIDColumn() 
    name = Column(String)

class QuestionModel(BaseModel):
    __tablename__ = 'questions'

    id = UUIDColumn() 
    name = Column(String) #kompletní znění otázky
    order = Column(Integer)
    survey_id = Column(ForeignKey('surveys.id'), primary_key=True)
    type_id = Column(ForeignKey('questionTypes.id'), primary_key=True)

class QuestionTypeModel(BaseModel):
    __tablename__ = 'questionTypes'
    id = UUIDColumn() 
    name = Column(String)


class AnswerModel(BaseModel):
    __tablename__ = 'answers'

    id = UUIDColumn()
    value = Column(String)
    aswered = Column(Boolean)
    expired = Column(Boolean)
    user_id = Column(ForeignKey('users.id'), primary_key=True)
    question_id = Column(ForeignKey('questions.id'), primary_key=True)


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
            try:
                await conn.run_sync(BaseModel.metadata.create_all)    
                print('BaseModel.metadata.create_all finished')
            except sqlalchemy.exc.NoReferencedTableError as e:
                print(e)
                print('Unable automaticaly create tables')
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
    database =  os.environ.get("POSTGRES_DB", "data")
    hostWithPort =  os.environ.get("POSTGRES_HOST", "postgres:5432")
    
    driver = "postgresql+asyncpg" #"postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring