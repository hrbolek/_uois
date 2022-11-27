from sqlalchemy.future import select
import strawberry

from gql_ug.DBDefinitions import BaseModel, UserModel, GroupModel, MembershipModel, RoleModel
from gql_ug.DBDefinitions import GroupTypeModel, RoleTypeModel

def AsyncSessionFromInfo(info):
    return info.context['session']

def UserFromInfo(info):
    return info.context['user']

class BasePermission(strawberry.permission.BasePermission):
    message = "User is not authenticated"
    
    async def has_permission(self, source, info: strawberry.types.Info, **kwargs) -> bool:
        print('BasePermission', source)
        print('BasePermission', self)
        print('BasePermission', kwargs)
        return True

class GroupEditorPermission(BasePermission):
    message = "User is not authenticated"
    
    async def canEditGroup(session, group_id, user_id):
        stmt = select(RoleModel).filter_by(group_id=group_id, user_id=user_id)
        dbRecords = await session.execute(stmt).scalars()
        dbRecords = [*dbRecords] # konverze na list
        if len(dbRecords) > 0 :
            return True
        else:
            return False

    async def has_permission(self, source, info: strawberry.types.Info, **kwargs) -> bool:
        print('GroupEditorPermission', source)
        print('GroupEditorPermission', self)
        print('GroupEditorPermission', kwargs)
        #_ = await self.canEditGroup(AsyncSessionFromInfo(info), source.id, ...)
        print('GroupEditorPermission')
        return True

class UserEditorPermission(BasePermission):
    message = "User is not authenticated"
    
    async def has_permission(self, source, info: strawberry.types.Info, **kwargs) -> bool:
        print('UserEditorPermission', source)
        print('UserEditorPermission', self)
        print('UserEditorPermission', kwargs)
        return True

class UserGDPRPermission(BasePermission):
    message = "User is not authenticated"
    
    async def has_permission(self, source, info: strawberry.types.Info, **kwargs) -> bool:
        print('UserGDPRPermission', source)
        print('UserGDPRPermission', self)
        print('UserGDPRPermission', kwargs)
        return True

