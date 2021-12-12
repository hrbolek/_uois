from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int

from models.GroupRelated.GroupTypeModel import GroupTypeModel
from graphqltypes.Utils import extractSession

class GroupTypeType(ObjectType):
    id = ID()
    name = String()

    groups = List('graphqltypes.Group.GroupType')
    def resolve_groups(parent, info):
        session = extractSession(info)
        groupTypeRecord = session.query(GroupTypeModel).get(parent.id)
        return groupTypeRecord.groups
        
