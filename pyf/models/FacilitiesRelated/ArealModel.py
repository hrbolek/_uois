import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship, backref
import datetime

from ..BaseModel import BaseModel

class ArealModel(BaseModel):
    __tablename__ = 'areals'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    lastchange = Column(DateTime, default=datetime.datetime.now)

    buildings = relationship('BuildingModel', back_populates='areal')
