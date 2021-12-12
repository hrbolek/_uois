from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
import datetime
from functools import cache

import sqlengine.sqlengine as SqlEngine

from . import BaseModel

@cache # funny thing, it makes from this function a singleton
def GetModels(BaseModel=BaseModel.getBaseModel(), unitedSequence=Sequence('all_id_seq')):
    """create elementary models for information systems

    Parameters
    ----------
    BaseModel
        represents the declarative_base instance from SQLAlchemy
    unitedSequence : Sequence
        represents a method for generating keys (usually ids) for database entities

    Returns
    -------
    (AreaModel, BuildingModel, RoomModel)
        tuple of models based on BaseModel, table names are hardcoded

    """

    assert not(unitedSequence is None), "unitedSequence must be defined"
    
    class ArealModel(BaseModel):
        __tablename__ = 'areals'

        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        lastchange = Column(DateTime, default=datetime.datetime.now)
        externalId = Column(Integer, index=True)

    class BuildingModel(BaseModel):
        __tablename__ = 'buildings'

        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        lastchange = Column(DateTime, default=datetime.datetime.now)
        externalId = Column(Integer, index=True)

    class RoomModel(BaseModel):
        __tablename__ = 'rooms'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        lastchange = Column(DateTime, default=datetime.datetime.now)
        externalId = Column(Integer, index=True)

    return ArealModel, BuildingModel, RoomModel

@cache
def BuildRelations():

    ArealModel, BuildingModel, RoomModel = GetModels()
    from . import Relations 

    Relations.defineRelation1N(ArealModel, BuildingModel)
    Relations.defineRelation1N(BuildingModel, RoomModel)
    pass

import random
def PopulateRandomData(SessionMaker):
    session = SessionMaker()
    
    ArealModel, BuildingModel, RoomModel = GetModels()

    numbers = [1, 2, 3, 4, 5, 7, 8, 9]
    firstLetters = ['A', 'C', 'L', 'K']
    def RandomizedRoom(areal, building, index):
        randomName = f'{index}'
        roomRecord = RoomModel(name=randomName)
        session.add(roomRecord)
        session.commit()
        pass

    def RandomizedBuilding(areal, index):
        randomName = f'B{index+1}'
        buildingRecord = BuildingModel(name=randomName)
        session.add(buildingRecord)
        session.commit()
        floors = random.randrange(2, 5)
        roomsPerFloor = random.randrange(10, 15)
        for floor in range(floors):
            for room in range(roomsPerFloor):
                RandomizedRoom(areal, buildingRecord, (floor + 1) * 100 + room)
        pass

    def RandomizedAreal():
        randomName = f'{random.choice(firstLetters)}{random.choice(numbers)}{random.choice(numbers)}'
        arealRecord = ArealModel(name=randomName)
        session.add(arealRecord)
        session.commit()
        buildingCount = random.randrange(5, 8)
        for _ in range(buildingCount):
            RandomizedBuilding(arealRecord, _)
        pass

    try:
        arealCount = random.randrange(3, 5)
        for _ in range(arealCount):
            RandomizedAreal()
        pass
    finally:
        session.close()