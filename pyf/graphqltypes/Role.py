from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int

from models.GroupRelated.RoleModel import RoleModel
from graphqltypes.Utils import extractSession

class RoleType(ObjectType):
    id = ID()

    lastchange = DateTime()
    externalId = String()

    user = Field('graphqltypes.User.UserType')
    group = Field('graphqltypes.Group.GroupType')
    def resolve_user(parent, info):
        session = extractSession(info)
        dbRecord = session.query(RoleModel).get(parent.id)
        return dbRecord.user
        
    def resolve_group(parent, info):
        session = extractSession(info)
        dbRecord = session.query(RoleModel).get(parent.id)
        return dbRecord.group
