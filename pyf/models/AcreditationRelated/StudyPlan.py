

import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
from sqlalchemy.orm import relationship
import datetime

from models.BaseModel import BaseModel
       
class StudyPlanModel(BaseModel):
    __tablename__ = 'studyplans'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

    studyplanitems = relationship('StudyPlanItemModel', back_populates='studyplan')
