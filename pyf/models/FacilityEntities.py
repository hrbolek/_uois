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
    
    class AreaModel(BaseModel):
        __tablename__ = 'areas'

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

    return AreaModel, BuildingModel, RoomModel

@cache
def BuildRelations():

    AreaModel, BuildingModel, RoomModel = GetModels()
    from . import Relations 

    Relations.defineRelation1N(AreaModel, BuildingModel)
    Relations.defineRelation1N(BuildingModel, RoomModel)
    pass