from pydantic import BaseModel as BaseSchema
from typing import List, Optional

from simpleschemas import UserGetSimpleSchema, GroupGetSimpleSchema, EventGetSimpleSchema, ClassRoomGetSimpleSchema

class EventGetSchema(EventGetSimpleSchema):
    users: List[UserGetSimpleSchema]
    groups: List[GroupGetSimpleSchema]
    classrooms: List[ClassRoomGetSimpleSchema]
    class Config:
        orm_mode = True