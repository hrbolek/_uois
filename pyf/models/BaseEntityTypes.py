from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
import datetime
from functools import cache

import sqlengine.sqlengine as SqlEngine

#unitedSequence = Sequence('all_id_seq')

@cache # funny thing, it makes from this function a singleton
def GetModels(BaseModel=SqlEngine.getBaseModel(), unitedSequence=Sequence('all_id_seq')):
    assert not(unitedSequence is None), "unitedSequence must be defined"
    
    class GroupTypeModel(BaseModel):
        __tablename__ = 'grouptypes'
        
        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)
        
    class RoleTypesModel(BaseModel):
        __tablename__ = 'roletypes'

        id = Column(BigInteger, unitedSequence, primary_key=True)
        name = Column(String)

    return GroupTypeModel, RoleTypesModel