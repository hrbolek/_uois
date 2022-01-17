from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int

from models.GroupRelated.RoleTypeModel import RoleTypeModel
from graphqltypes.Utils import extractSession
from graphqltypes.Utils import createRootResolverById, createRootResolverByName

RoleTypeRootResolverById = createRootResolverById(RoleTypeModel)
RoleTypeRootResolverByName = createRootResolverByName(RoleTypeModel)

class RoleTypeType(ObjectType):
    id = ID()
    name = String()

    roles = List('graphqltypes.Role.RoleType')
    def resolve_roles(parent, info):
        session = extractSession(info)
        dbRecord = session.query(RoleTypeModel).get(parent.id)
        try:
            result = dbRecord.roles
        except Exception as e:
            print(e)
        return result
        
