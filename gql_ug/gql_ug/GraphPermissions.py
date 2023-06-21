from sqlalchemy.future import select
import strawberry

from gql_ug.DBDefinitions import (
    BaseModel,
    UserModel,
    GroupModel,
    MembershipModel,
    RoleModel,
)
from gql_ug.DBDefinitions import GroupTypeModel, RoleTypeModel


def AsyncSessionFromInfo(info):
    return info.context["session"]


def UserFromInfo(info):
    return info.context["user"]



import os
import aiohttp

GQL_PROXY = os.environ.get("GQL_PROXY", "http://localhost:31180/api/gql") # http://apollo:3000/api/gql/
print("GQL_PROXY", GQL_PROXY)
async def getUserFromHeaders(headers):
    user = {
        "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"
    }

    if os.environ.get("DEMO", None) == "true":
        user = {
            "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
            "name": "John",
            "surname": "Newbie",
            "email": "john.newbie@world.com",
            "roles": [
                {
                "valid": True,
                "group": {
                    "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                    "name": "Uni"
                },
                "roletype": {
                    "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                    "name": "administrátor"
                }
                },
                {
                "valid": True,
                "group": {
                    "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                    "name": "Uni"
                },
                "roletype": {
                    "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
                    "name": "rektor"
                }
                }
            ]
        }
    else:
        pass

    gqlQuery = {"query": '''
        query($id: ID!){
            result: userById(id: $id) {
                id
                name
                surname
                email
                roles {
                valid
                group { id name }
                roletype { id name }
                }
            }
        }
    '''}
    gqlQuery["variables"] = {"id": user["id"]}

    # print(demoquery)
    headers = {}
    async with aiohttp.ClientSession() as session:
        
        async with session.post(GQL_PROXY, json=gqlQuery, headers=headers) as resp:
            
            json = await resp.json()        
            print("gqlQuery", gqlQuery, flush=True)
            print("resp.status", resp.status, flush=True)
            print(json)
    user = json["data"]["result"]
    print("Permission for user", user, flush=True)

    return user


class BasePermission(strawberry.permission.BasePermission):
    message = "User is not authenticated"

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        print("BasePermission", source)
        print("BasePermission", self)
        print("BasePermission", kwargs)
        return True


class GroupEditorPermission(BasePermission):
    message = "User is not authenticated"

    async def canEditGroup(session, group_id, user_id):
        stmt = select(RoleModel).filter_by(group_id=group_id, user_id=user_id)
        dbRecords = await session.execute(stmt).scalars()
        dbRecords = [*dbRecords]  # konverze na list
        if len(dbRecords) > 0:
            return True
        else:
            return False

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        print("GroupEditorPermission", source)
        print("GroupEditorPermission", self)
        print("GroupEditorPermission", kwargs)
        # _ = await self.canEditGroup(session,  source.id, ...)
        print("GroupEditorPermission")
        return True


class UserEditorPermission(BasePermission):
    message = "User is not authenticated"

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        print("UserEditorPermission", source)
        print("UserEditorPermission", self)
        print("UserEditorPermission", kwargs)
        return True

def getLoader(info):
    return info.context["all"]

import asyncio

def WhereAuthorized(user, rolesNeeded):
    roleIdsNeeded = list(map(lambda item: item["id"], rolesNeeded))
    print("roleIdsNeeded", roleIdsNeeded)
    # 👇 filtrace roli, ktere maji pozadovanou uroven autorizace
    roletypesFiltered = filter(lambda item: item["roletype"]["id"] in roleIdsNeeded, user["roles"])
    # 👇 odvozeni, pro ktere skupiny ma tazatel patricnou uroven autorizace
    groupsAuthorizedIds = map(lambda item: item["group"]["id"], roletypesFiltered)
    # 👇 konverze na list
    groupsAuthorizedIds = list(groupsAuthorizedIds)
    print("groupsAuthorizedIds", groupsAuthorizedIds)
    return groupsAuthorizedIds

from functools import cache
class UserGDPRPermission(BasePermission):
    message = "User has not proper rights"

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        
        loader = getLoader(info).memberships
        
        # 👇 kdo se pta, a jake role ma
        userAwaitable = getUserFromHeaders({})       
        # 👇 na koho se pta a v jakych skupinach je clenem
        membershipsAwaitable = loader.filter_by(user_id=source.id)
        # 👇 soubeh dotazu
        [user, memberships, *_] = await asyncio.gather(userAwaitable, membershipsAwaitable)
        
        # 👇 jake role jsou nutne pro ziskani informace
        rolesNeeded = [{'id': 'ced46aa4-3217-4fc1-b79d-f6be7d21c6b6', 'name': 'administrátor'}, {'id': 'ae3f0d74-6159-11ed-b753-0242ac120003', 'name': 'rektor'}]      
        # 👇 id skupin, kde ma tazatel pozadovane opravneni
        groupsAuthorizedIds = WhereAuthorized(user, rolesNeeded=rolesNeeded)

        # 👇 id skupin, kde je cil clenem
        userGroupIds = list(map(lambda item: item.group_id, memberships))
        print("userGroupIds", userGroupIds)
        # 👇 filtrace skupin, kde je cil clenem a kde ma tazatel autorizaci
        groupidsIntersection = filter(lambda item: item in groupsAuthorizedIds, userGroupIds)
        # 👇 je zde alespon jeden prunik?
        isAuthorized = next(groupidsIntersection, None) is not None
        print("isAuthorized", isAuthorized)

        print("UserGDPRPermission.user", user)
        print("UserGDPRPermission.source", source.id) # SQLAlchemyModel
        print("UserGDPRPermission.self", self) # GQLModel
        print("UserGDPRPermission.kwargs", kwargs) # resolver parameters
        # return True
        return isAuthorized


