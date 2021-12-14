import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
import datetime

from models.BaseModel import BaseModel

#from models.FacilitiesRelated.RoomModel import RoomModel

# EventRoomModel = Table('events_rooms', BaseModel.metadata,
#         Column('id', BigInteger, Sequence('all_id_seq'), primary_key=True),
#         Column('room_id', ForeignKey('rooms.id'), primary_key=True),
#         Column('event_id', ForeignKey('events.id'), primary_key=True)

# )

class EventRoomModel(BaseModel):
        __tablename__ = 'events_rooms'

        id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
        room_id = Column(ForeignKey('rooms.id'), primary_key=True)
        event_id = Column(ForeignKey('events.id'), primary_key=True)
