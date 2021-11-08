from typing import List, Optional
from pydantic import BaseModel as BaseSchema

import datetime

class UserGetSimpleSchema(BaseSchema):
    id: int
    name: str
    externalId: str
    class Config:
        orm_mode = True

class GroupGetSimpleSchema(BaseSchema):
    id: int
    name: str
    externalId: Optional[str] = ''
    class Config:
        orm_mode = True
        
class EventGetSimpleSchema(BaseSchema):
    id: int
    label: str
    start: datetime.datetime
    end: datetime.datetime
    class Config:
        orm_mode = True
    
class ClassRoomGetSimpleSchema(BaseSchema):
    id: int
    name: str
    externalId: str
    class Config:
        orm_mode = True