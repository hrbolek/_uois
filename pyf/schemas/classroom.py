from pydantic import BaseModel as BaseSchema

from simpleschemas import UserGetSimpleSchema, GroupGetSimpleSchema, EventGetSimpleSchema, ClassRoomGetSimpleSchema

class ClassRoomGetSchema(ClassRoomGetSimpleSchema):

    class Config:
        orm_mode = True