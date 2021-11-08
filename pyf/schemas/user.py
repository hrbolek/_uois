from pydantic import BaseModel as BaseSchema

from simpleschemas import UserGetSimpleSchema, GroupGetSimpleSchema, EventGetSimpleSchema, ClassRoomGetSimpleSchema
from typing import List, Optional

class UserGetSchema(UserGetSimpleSchema):
    groups: List[GroupGetSimpleSchema]
        
    class Config:
        orm_mode = True