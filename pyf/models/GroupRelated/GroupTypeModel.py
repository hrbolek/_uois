import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship, backref
import datetime

from models.BaseModel import BaseModel

class GroupTypeModel(BaseModel):
    __tablename__ = 'grouptypes'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

    groups = relationship('GroupModel', back_populates='grouptype')
