import os
import uuid
import hashlib
import json
import sqlalchemy
import logging
from functools import cache
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Uuid, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from uoishelpers.dataloaders import createIdLoader

BaseModel = declarative_base()

class UserModel(BaseModel):
    __tablename__ = "user_credentials"
    # id = Column(Uuid, primary_key=True, comment="primary key", default=uuid.uuid1)
    id = Column(String, primary_key=True, comment="primary key")
    email = Column(String)
    password = Column(String)

def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
    Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "host.docker.internal:5432")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring

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

def createLoader(asyncSessionMaker):
    return createIdLoader(asyncSessionMaker, UserModel)

@cache
def getsalt():
    result = os.environ.get("SALT", None)
    assert result is not None, "SALT environment variable must be explicitly defined"
    return result.encode(encoding="utf-8")

def hashfunction(value= " "):
    result = hashlib.pbkdf2_hmac('sha256', value.encode('utf-8'), getsalt(), 100000)    
    return result.hex()

async def passwordValidator(asyncSessionMaker, email, rawpassword):
    loader = createLoader(asyncSessionMaker)
    hashedpassword = hashfunction(rawpassword)
    rows = await loader.filter_by(email=email)
    row = next(rows, None)
    logging.info(f"passwordValidator loader returns {row} for email {email}")
    return False if row is None else row.password == hashedpassword

async def emailMapper(asyncSessionMaker, email):
    loader = createLoader(asyncSessionMaker)
    rows = await loader.filter_by(email=email)
    row = next(rows, None)
    return None if row is None else row.id

def getDemoData():
    with open("./systemdata.json", "r", encoding="utf-8") as f:
        jsonData = json.load(f)
    return jsonData

async def initDB(asyncSessionMaker):
    DEMO = os.environ.get("DEMO", None)
    assert DEMO is not None, "DEMO environment variable must be explicitly defined"
    if DEMO in ["True", True, "False", False]:
        logging.info(f"Inserting users into DB")

    # if True:
        jsonData = getDemoData()

        loader = createLoader(asyncSessionMaker)
        table = jsonData["users"]
        for row in table:
            email = row.get("email", None)
            assert email is not None, f"user {row} has no email"
            password = row.get("password", email)
            hashedpassword = hashfunction(password)
            id = row.get("id", None)
            assert id is not None, f"user {row} has no id"
            user = UserModel(id=id, email=email, password=hashedpassword)
            row = await loader.load(id)
            logging.info(f"got {row}")
            try:
                logging.info(f"{user} [{user.email}] inserting in DB")
                await loader.insert(user)
                logging.info(f"{user} inserted in DB")
            except:
                pass

