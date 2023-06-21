from sqlalchemy.future import select
import strawberry

from gql_externalids.DBDefinitions import (
    BaseModel,
)

def AsyncSessionFromInfo(info):
    return info.context["session"]


def UserFromInfo(info):
    return info.context["user"]

import os
import aiohttp

GQL_PROXY = os.environ.get("GQL_PROXY", "http://localhost:31180/api/gql") # http://apollo:3000/api/gql/
async def getUserFromHeaders(headers):
    user = {
        "id": "f8089aa6-2c4a-4746-9503-105fcc5d054c"
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
                # print(resp.status)
                json = await resp.json()        
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


class UserGDPRPermission(BasePermission):
    message = "User is not authenticated"

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        print("UserGDPRPermission", source)
        print("UserGDPRPermission", self)
        print("UserGDPRPermission", kwargs)
        return True
