import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship, backref
import datetime

from ..BaseModel import BaseModel

class BuildingModel(BaseModel):
    __tablename__ = 'buildings'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)
    
    lastchange = Column(DateTime, default=datetime.datetime.now)

    rooms = relationship('RoomModel', back_populates='building')

    areal_id = Column(ForeignKey('areals.id'))
    areal = relationship('ArealModel', back_populates='buildings')