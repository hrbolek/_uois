from pydantic import BaseModel as BaseSchema
from typing import List, Optional

from simpleschemas import UserGetSimpleSchema, GroupGetSimpleSchema, EventGetSimpleSchema, ClassRoomGetSimpleSchema

class GroupGetSchema(GroupGetSimpleSchema):
    users: List[UserGetSimpleSchema]
    
    class Config:
        orm_mode = True