from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int
from functools import cache
from graphqltypes.Utils import attachResolverForRelationNM, extractSession, attachResolverForRelation1N, createResolver

@cache
def GetTypes(UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel):

    class UserType(ObjectType):
        id = ID()
        name = String()
        surname = String()
        email = String()

        lastchange = DateTime()
        externalId = String()

    class GroupType(ObjectType):
        name = String()
        id = ID()
        grouptype_id = ID()

        entryYearId = Int()
        lastchange = DateTime()
        externalId = String()

    class GroupTypeType(ObjectType):
        id = ID()
        name = String()

    class RoleType(ObjectType):
        id = ID()
        name = String()
        lastchange = DateTime()

    class RoleTypeType(ObjectType):
        id = ID()
        name = String()


    attachResolverForRelationNM(UserType, GroupType, 'groups', 'users', createResolver(UserModel, 'groups'), createResolver(GroupModel, 'users'))
    attachResolverForRelation1N(GroupTypeType, GroupType, 'groups', 'grouptype', createResolver(GroupTypeModel, 'groups'), createResolver(GroupModel, 'grouptype'))

    attachResolverForRelation1N(RoleTypeType, RoleType, 'roles', 'roletype', createResolver(RoleTypeModel, 'roles'), createResolver(RoleModel, 'roletype'))
    attachResolverForRelation1N(UserType, RoleType, 'roles', 'users', createResolver(UserModel, 'roles'), createResolver(RoleModel, 'user'))
    attachResolverForRelation1N(GroupType, RoleType, 'roles', 'groups', createResolver(GroupModel, 'roles'), createResolver(RoleModel, 'group'))


    class UserTypeRel(UserType):
        pass
    class GroupTypeRel(GroupType):
        pass
    class GroupTypeTypeRel(GroupTypeType):
        pass
    class RoleTypeTypeRel(RoleTypeType):
        pass
    class RoleTypeRel(RoleType):
        pass

    return UserTypeRel, GroupTypeRel, RoleTypeRel, GroupTypeTypeRel, RoleTypeTypeRel
        