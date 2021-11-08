from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
import datetime
from functools import cache

import sqlengine.sqlengine as SqlEngine

#unitedSequence = Sequence('all_id_seq')

@cache # funny thing, it makes from this function a singleton
def GetModels(BaseModel=SqlEngine.getBaseModel(), unitedSequence=Sequence('all_id_seq')):
    #assert not(unitedSequence is None), "unitedSequence must be defined"

    class UserModel(BaseModel):
        __tablename__ = 'users'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
        lastchange = Column(DateTime, default=datetime.datetime.now)
        externalId = Column(BigInteger, index=True)


    class GroupModel(BaseModel):
        __tablename__ = 'groups'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
        lastchange = Column(DateTime, default=datetime.datetime.now)
        entryYearId = Column(Integer)

        externalId = Column(String, index=True)
        
        
    class ClassRoomModel(BaseModel):
        __tablename__ = 'classrooms'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        area_id = Column(Integer)
        lastchange = Column(DateTime, default=datetime.datetime.now)
        externalId = Column(Integer, index=True)
        
        
    class EventModel(BaseModel):
        __tablename__ = 'events'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        start = Column(DateTime)
        end = Column(DateTime)
        label = Column(String)
        externalId = Column(String, index=True)
        lastchange = Column(DateTime, default=datetime.datetime.now)


    return UserModel, GroupModel, ClassRoomModel, EventModel
