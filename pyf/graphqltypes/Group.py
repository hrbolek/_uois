from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int

from models.GroupRelated.GroupModel import GroupModel
from graphqltypes.Utils import extractSession

from graphqltypes.Utils import createRootResolverById, createRootResolverByName

GroupRootResolverById = createRootResolverById(GroupModel)
GroupRootResolverByName = createRootResolverByName(GroupModel)

class GroupType(ObjectType):
    id = ID()
    name = String()

    lastchange = DateTime()
    externalId = String()

    users = List('graphqltypes.User.UserType')
    def resolve_users(parent, info):
        session = extractSession(info)
        groupRecord = session.query(GroupModel).get(parent.id)
        return groupRecord.users
        
