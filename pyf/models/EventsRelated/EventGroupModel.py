import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
import datetime

from ..BaseModel import BaseModel
       
#from models.GroupRelated.GroupModel import GroupModel

# EventGroupModel = Table('events_groups', BaseModel.metadata,
#         Column('id', BigInteger, Sequence('all_id_seq'), primary_key=True),
#         Column('group_id', ForeignKey('groups.id'), primary_key=True),
#         Column('event_id', ForeignKey('events.id'), primary_key=True)

# )

class EventGroupModel(BaseModel):
        __tablename__ = 'events_groups'

        id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
        group_id = Column(ForeignKey('groups.id'), primary_key=True)
        event_id = Column(ForeignKey('events.id'), primary_key=True)