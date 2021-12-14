import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship, backref
import datetime

from ..BaseModel import BaseModel

class RoomModel(BaseModel):
    __tablename__ = 'rooms'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    lastchange = Column(DateTime, default=datetime.datetime.now)

    building_id = Column(ForeignKey('buildings.id'))
    building = relationship('BuildingModel', back_populates='rooms')