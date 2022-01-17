import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship, backref
import datetime

from models.BaseModel import BaseModel

class RoleTypeModel(BaseModel):
    __tablename__ = 'roletypes'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

    roles = relationship('RoleModel', back_populates='roletype')
