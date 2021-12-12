import types
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
import datetime

from models.BaseModel import BaseModel
       
class AcreditationUserRoleModel(BaseModel):
    __tablename__ = 'acreditationuserrole'
    
    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)