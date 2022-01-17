import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
import datetime

from models.BaseModel import BaseModel
#from models.GroupRelated.UserModel import UserModel

# EventUserModel = Table('events_users', BaseModel.metadata,
#         Column('id', BigInteger, Sequence('all_id_seq'), primary_key=True),
#         Column('user_id', ForeignKey('users.id'), primary_key=True),
#         Column('event_id', ForeignKey('events.id'), primary_key=True)

# )

class EventUserModel(BaseModel):
        __tablename__ = 'events_users'

        id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
        user_id = Column(ForeignKey('users.id'), primary_key=True)
        event_id = Column(ForeignKey('events.id'), primary_key=True)
