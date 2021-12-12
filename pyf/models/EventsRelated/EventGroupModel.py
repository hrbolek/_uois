import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
import datetime

from ..BaseModel import BaseModel
       
EventGroupModel = Table('events_groups', BaseModel.metadata,
        Column('id', BigInteger, Sequence('all_id_seq'), primary_key=True),
        Column('group_id', ForeignKey('groups.id'), primary_key=True),
        Column('group_id', ForeignKey('events.id'), primary_key=True)

)