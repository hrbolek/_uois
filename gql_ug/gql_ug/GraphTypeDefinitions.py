import typing
from typing import List, Union, Optional
import strawberry as strawberryA
import uuid
import datetime

from contextlib import asynccontextmanager


@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


def getLoader(info):
    return info.context["all"]


import datetime
from gql_ug.GraphResolvers import resolveMembershipById

# @strawberryA.federation.type(
#     keys=["id"],
#     description="""Entity representing a relation between an user and a group""",
# )
# class UGInsertGQLModel:
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info):
#         result = UGInsertGQLModel()
#         return result

#     @strawberryA.field(description="""Inserts new membership""")
#     async def id(self) -> strawberryA.ID:
#         return 1

#     @strawberryA.field(description="""Inserts new membership""")
#     async def membership_insert(self, 
#         info: strawberryA.types.Info, 
#         membership: "MembershipInsertGQLModel"
#     ) -> "MembershipResultGQLModel":

#         loader = getLoader(info).memberships
#         row = await loader.insert(membership)

#         result = MembershipResultGQLModel()
#         result.msg = "ok"
#         result.id = row.id
        
#         return result

#     @strawberryA.field(description="""Inserts new user""")
#     async def user_insert(self, info: strawberryA.types.Info, user: "UserInsertGQLModel") -> "UserResultGQLModel":
#         loader = getLoader(info).users
        
#         row = await loader.insert(user)

#         result = UserResultGQLModel()
#         result.id = row.id
#         result.msg = "ok"
        
#         return result

#     @strawberryA.field(description="""
#         Allows a update of group, also it allows to change the mastergroup of the group
#     """)
#     async def group_insert(self, info: strawberryA.types.Info, group: "GroupInsertGQLModel") -> "GroupResultGQLModel":
#         loader = getLoader(info).groups
        
#         updatedrow = await loader.insert(group)
#         print("group_insert", updatedrow, updatedrow.id, updatedrow.name, flush=True)
#         result = GroupResultGQLModel()
#         result.id = updatedrow.id
#         result.msg = "ok"

#         if updatedrow is None:
#             result.msg = "fail"
        
#         return result

#     @strawberryA.field(description="""
#         Inserts a group
#     """)
#     async def group_type_insert(self, info: strawberryA.types.Info, group_type: "GeneralTypeInsertGQLModel") -> "GroupTypeResultGQLModel":
#         loader = getLoader(info).grouptypes
        
#         updatedrow = await loader.insert(group_type)
#         result = GroupTypeResultGQLModel()
#         result.id = updatedrow.id
#         result.msg = "ok"

#         if updatedrow is None:
#             result.msg = "fail"
        
#         return result

#     @strawberryA.field(description="""Inserts a role""")
#     async def role_insert(self, 
#         info: strawberryA.types.Info, 
#         role: "RoleInsertGQLModel"
#     ) -> "RoleResultGQLModel":

#         loader = getLoader(info).roles

#         result = RoleResultGQLModel()
#         result.msg = "ok"
        
#         updatedrow = await loader.insert(role)
#         result.id = updatedrow.id
        
#         return result

#     @strawberryA.field(description="""Inserts a new roleType record""")
#     async def role_type_insert(self, 
#         info: strawberryA.types.Info, 
#         role_type: "GeneralTypeInsertGQLModel"

#     ) -> "RoleTypeResultGQLModel":
#         #print("role_type_update", role_type, flush=True)
#         loader = getLoader(info).roletypes
#         row = await loader.insert(role_type)
#         if row is not None:
#             print("role_type_update", row, row.name, row.id, flush=True)
#         result = RoleTypeResultGQLModel()
#         result.msg = "ok"
#         result.id = row.id       
#         return result
   
#     @strawberryA.field(description="""Inserts a role category""")
#     async def role_category_insert(self, 
#         info: strawberryA.types.Info, 
#         role_category: "GeneralTypeInsertGQLModel"

#     ) -> "RoleCategoryResultGQLModel":

#         loader = getLoader(info).rolecategories
#         row = await loader.insert(role_category)

#         result = RoleCategoryResultGQLModel()
#         result.msg = "ok"
#         result.id = row.id
        
#         return result


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class MembershipGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoader(info).memberships
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""time stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""user""")
    async def user(self, info: strawberryA.types.Info) -> "UserGQLModel":
        # return self.user
        result = await UserGQLModel.resolve_reference(info=info, id=self.user_id)
        return result

    @strawberryA.field(description="""group""")
    async def group(self, info: strawberryA.types.Info) -> "GroupGQLModel":
        # return self.group
        result = await GroupGQLModel.resolve_reference(info=info, id=self.group_id)
        return result

    @strawberryA.field(description="""is the membership is still valid""")
    async def valid(self) -> Union[bool, None]:
        return self.valid

    @strawberryA.field(description="""date when the membership begins""")
    async def startdate(self) -> Union[datetime.datetime, None]:
        return self.startdate

    @strawberryA.field(description="""date when the membership ends""")
    async def enddate(self) -> Union[datetime.datetime, None]:
        return self.enddate

    # @strawberryA.field(description="""date when the membership ends""")
    # async def editor(self) -> "MembershipEditorGQLModel":
    #     return self

# @strawberryA.federation.type(
#     keys=["id"],
#     description="""Entity representing a relation between an user and a group""",
# )
# class MembershipEditorGQLModel: 
#     @classmethod
#     async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
#         loader = getLoader(info).memberships
#         result = await loader.load(id)
#         if result is not None:
#             result._type_definition = cls._type_definition  # little hack :)
#         return result

#     @strawberryA.field(description="""primary key""")
#     def id(self) -> strawberryA.ID:
#         return self.id

#     @strawberryA.mutation(description="""Update the membership, cannot update group / user""")
#     async def update(self, 
#         info: strawberryA.types.Info, 
#         membership: "MembershipUpdateGQLModel"
#     ) -> "MembershipResultGQLModel":

#         loader = getLoader(info).memberships
#         updatedrow = await loader.update(membership)

#         result = MembershipResultGQLModel()
#         result.msg = "ok"
#         result.id = membership.id

#         if updatedrow is None:
#             result.msg = "fail"
       
#         return result


from gql_ug.GraphResolvers import resolveMembershipForUser, resolveRolesForUser
from gql_ug.GraphResolvers import resolveUserById
from gql_ug.GraphResolvers import resolveUsersById, resolveGroupsById
from gql_ug.GraphResolvers import membershipsSelect


@strawberryA.federation.type(keys=["id"], description="""Entity representing a user""")
class UserGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        # userloader = info.context['users']
        loader = getLoader(info).users
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self, info: strawberryA.types.Info) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""User's name (like John)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""User's family name (like Obama)""")
    def surname(self) -> str:
        return self.surname

    @strawberryA.field(description="""User's email""")
    def email(self) -> Union[str, None]:
        return self.email

    @strawberryA.field(description="""User's validity (if their are member of institution)""")
    def valid(self) -> bool:
        return self.valid

    @strawberryA.field(description="""Time stamp""")
    def lastchange(self) -> Union[datetime.datetime, None]:
        return self.lastchange

    @strawberryA.field(description="""List of groups, where the user is member""")
    async def membership(
        self, info: strawberryA.types.Info
    ) -> typing.List["MembershipGQLModel"]:
        # membershiploader = info.context['memberships']
        # selectstmt = membershipsSelect.filter_by(user_id=self.id)
        # result = await membershiploader.execute_select(selectstmt)

        loader = getLoader(info).memberships
        #print(self.id)
        result = await loader.filter_by(user_id=self.id)
        return list(result)

    #        statement =
    # result = await resolveMembershipForUser(session,  self.id)
    # async with withInfo(info) as session:
    #     result = await resolveMembershipForUser(session, self.id)
    #     return result

    @strawberryA.field(description="""List of roles, which the user has""")
    async def roles(self, info: strawberryA.types.Info) -> typing.List["RoleGQLModel"]:
        loader = getLoader(info).roles
        result = await loader.filter_by(user_id=self.id)
        return result

    @strawberryA.field(
        description="""List of groups given type, where the user is member"""
    )
    async def member_of(
        self, grouptype_id: strawberryA.ID, info: strawberryA.types.Info
    ) -> typing.List["GroupGQLModel"]:
        """type hinting pouziva strawberry ke spravne deserializaci, vysledek deserializace ma vliv na operatory (napr. __EQ__)
        v tomto pripade je mozne primo srovnavat, pokud by jako hint typ u grouptype_id byl str, muselo by se srovnavat jinak
        """
        async with withInfo(info) as session:
            memberships = await resolveMembershipForUser(session, self.id)
            result = [
                membership.group
                for membership in memberships
                if membership.group.grouptype_id == grouptype_id
            ]
            return result

    @strawberryA.field(description="""returns the user editor if possible""")
    async def editor(
        self, info: strawberryA.types.Info
    ) -> Union["UserEditorGQLModel", None]:
        ## current user must be checked if has rights to get the editor
        ## if not, then None value must be returned
        return self


# @strawberryA.input
# class UserUpdateGQLModel:
#     lastchange: datetime.datetime  # razitko
#     name: Optional[str] = None
#     surname: Optional[str] = None
#     email: Optional[str] = None
#     valid: Optional[bool] = None


# @strawberryA.input
# class UserInsertGQLModel:
#     id: Optional[strawberryA.ID] = None
#     name: Optional[str] = None
#     surname: Optional[str] = None
#     email: Optional[str] = None
#     valid: Optional[bool] = None


from gql_ug.GraphResolvers import resolverUpdateUser


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an editable user"""
)
class UserEditorGQLModel:
    ##
    ## Mutace, obejiti problemu s federativnim API
    ##

    # vysledky opearace update
    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await UserGQLModel.resolve_reference(info, id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result of update operation""")
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Result of update operation""")
    async def user(self, info: strawberryA.types.Info) -> UserGQLModel:
        result = await UserGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Updates the user data""")
    async def update(
        self, info: strawberryA.types.Info, data: "UserUpdateGQLModel"
    ) -> "UserEditorGQLModel":
        lastchange = data.lastchange
        # await resolverUpdateUser(session,  id=self.id, data=data)
        async with withInfo(info) as session:
            await resolverUpdateUser(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = UserEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result


import datetime
from gql_ug.GraphResolvers import (
    resolveMembershipForGroup,
    resolveMastergroupForGroup,
    resolveSubgroupsForGroup,
    resolveRolesForGroup,
)
from gql_ug.GraphResolvers import resolveGroupById
from gql_ug.GraphPermissions import GroupEditorPermission


@strawberryA.federation.type(keys=["id"], description="""Entity representing a group""")
class GroupGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        # result = await resolveGroupById(session,  id)
        # async with withInfo(info) as session:
        #     result = await resolveGroupById(session, id)
        #     result._type_definition = cls._type_definition # little hack :)
        #     return result

        loader = getLoader(info).groups
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(
        description="""Group's name (like Department of Intelligent Control)"""
    )
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Group's validity (still exists?)""")
    def valid(self) -> bool:
        if not self.valid:
            return False
        else:
            return self.valid

    @strawberryA.field(description="""""")
    def lastchange(self) -> Union[datetime.datetime, None]:
        result = self.lastchange
        return result

    @strawberryA.field(description="""Group's type (like Department)""")
    async def grouptype(
        self, info: strawberryA.types.Info
    ) -> Union["GroupTypeGQLModel", None]:
        loader = getLoader(info).grouptypes
        result = await loader.load(self.grouptype_id)
        return result

    @strawberryA.field(description="""Directly commanded groups""")
    async def subgroups(
        self, info: strawberryA.types.Info
    ) -> typing.List["GroupGQLModel"]:
        # result = await resolveSubgroupsForGroup(session,  self.id)
        # async with withInfo(info) as session:
        #     result = await resolveSubgroupsForGroup(session, self.id)

        #     return result

        loader = getLoader(info).groups
        print(self.id)
        result = await loader.filter_by(mastergroup_id=self.id)
        return list(result)

    @strawberryA.field(description="""Commanding group""")
    async def mastergroup(
        self, info: strawberryA.types.Info
    ) -> typing.Union["GroupGQLModel", None]:
        if self.mastergroup_id is None:
            return None
        else:
            result = await GroupGQLModel.resolve_reference(
                info=info, id=self.mastergroup_id
            )
            return result

    @strawberryA.field(description="""List of users who are member of the group""")
    async def memberships(
        self, info: strawberryA.types.Info
    ) -> typing.List["MembershipGQLModel"]:
        # result = await resolveMembershipForGroup(session,  self.id, skip, limit)
        # async with withInfo(info) as session:
        #     result = await resolveMembershipForGroup(session, self.id, skip, limit)
        #     return result

        loader = getLoader(info).memberships
        #print(self.id)
        result = await loader.filter_by(group_id=self.id)
        return list(result)

    @strawberryA.field(description="""List of roles in the group""")
    async def roles(self, info: strawberryA.types.Info) -> typing.List["RoleGQLModel"]:
        # result = await resolveRolesForGroup(session,  self.id)
        async with withInfo(info) as session:
            result = await resolveRolesForGroup(session, self.id)
            return result

    @strawberryA.field(
        # permission_classes=[GroupEditorPermission],
        description="""List of roles in the group"""
    )
    async def editor(
        self, info: strawberryA.types.Info
    ) -> Union["GroupEditorGQLModel", None]:
        # check if user has right to get editor (can edit this group)
        # if hasNoRight:
        #    return None
        # else:
        return self


from typing import Optional


# @strawberryA.input
# class GroupUpdateGQLModel:
#     lastchange: datetime.datetime
#     name: Optional[str] = None
#     type_id: Optional[strawberryA.ID] = None
#     valid: Optional[bool] = None


# @strawberryA.input
# class GroupInsertGQLModel:
#     id: Optional[strawberryA.ID] = None
#     name: Optional[str] = None
#     type_id: Optional[strawberryA.ID] = None
#     valid: Optional[bool] = None


from gql_ug.GraphResolvers import (
    resolveUpdateGroup,
    resolverRoleById,
    resolveInsertRole,
    resolveInsertMembership,
    resolveMembershipById,
)
from gql_ug.GraphResolvers import resolveInsertUser, resolveInsertGroup


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing an editable group"""
)
class GroupEditorGQLModel:
    ##
    ## Mutace, obejiti problemu s federativnim API
    ##
    ##
    ## Editor je rozšiřitelný v jiných prvcích federace.

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        # result = await resolveGroupById(session,  id)
        async with withInfo(info) as session:
            result = await resolveGroupById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(
        description="""Description of operation (group update) result. "ok", if all went good."""
    )
    def result(self) -> str:
        return self.result

    @strawberryA.field(description="""Link to the group.""")
    async def group(self, info: strawberryA.types.Info) -> GroupGQLModel:
        # result = await resolveGroupById(session,  self.id)
        async with withInfo(info) as session:
            result = await resolveGroupById(session, self.id)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Create a new membership""")
    async def add_membership(
        self, info: strawberryA.types.Info, user_id: strawberryA.ID
    ) -> "MembershipGQLModel":
        # result = await resolveInsertMembership(session,  None,
        #    extraAttributes={'user_id': user_id, 'group_id': self.id})

        async with withInfo(info) as session:
            result = await resolveInsertMembership(
                session, None, extraAttributes={"user_id": user_id, "group_id": self.id}
            )
            return result

    @strawberryA.field(description="""Invalidate a new membership""")
    async def invalidate_membership(
        self, info: strawberryA.types.Info, membership_id: strawberryA.ID
    ) -> "MembershipGQLModel":
        # session = AsyncSessionFromInfo(info)
        # role = await resolveMembershipById(session, membership_id)
        async with withInfo(info) as session:
            role = await resolveMembershipById(session, membership_id)
            role.valid = False
            await session.commit()
            return role

    @strawberryA.field(description="""Create a new role""")
    async def add_role(
        self,
        info: strawberryA.types.Info,
        user_id: strawberryA.ID,
        roletype_id: strawberryA.ID,
    ) -> "RoleGQLModel":
        # result = await resolveInsertRole(session,  None,
        #    extraAttributes={'user_id': user_id, 'group_id': self.id, 'roletype_id': roletype_id})
        async with withInfo(info) as session:
            result = await resolveInsertRole(
                session,
                None,
                extraAttributes={
                    "user_id": user_id,
                    "group_id": self.id,
                    "roletype_id": roletype_id,
                    "valid": True,
                },
            )
        return await RoleGQLModel.resolve_reference(info, id=result.id)
            

    @strawberryA.field(description="""Invalidate a new role""")
    async def invalidate_role(
        self, info: strawberryA.types.Info, role_id: strawberryA.ID
    ) -> "RoleGQLModel":
        # session = AsyncSessionFromInfo(info)
        # role = await resolverRoleById(session, role_id)
        async with withInfo(info) as session:
            role = await resolverRoleById(session, role_id)
            role.valid = False
            await session.commit()
            return role

    @strawberryA.field(description="""Create a new role""")
    async def create_subgroup(
        self, info: strawberryA.types.Info, group: "GroupInsertGQLModel"
    ) -> "GroupGQLModel":
        # newGroup = await resolveInsertGroup(session,  group, extraAttributes={'mastergroup_id': self.id})
        async with withInfo(info) as session:
            newGroup = await resolveInsertGroup(
                session, group, extraAttributes={"mastergroup_id": self.id}
            )
            print(newGroup)
            return newGroup

    @strawberryA.field(description="""Makes a group subgroup""")
    async def assign_subgroup(
        self, info: strawberryA.types.Info, subgroup_id: strawberryA.ID
    ) -> "GroupGQLModel":
        # updated = await resolveUpdateGroup(session,  subgroup_id, )
        # updated = await resolveUpdateGroup(session,  subgroup_id, data=None, extraAttributes={'mastergroup_id': self.id})
        async with withInfo(info) as session:
            updated = await resolveUpdateGroup(
                session,
                subgroup_id,
                data=None,
                extraAttributes={"mastergroup_id": self.id},
            )
            return self

    @strawberryA.field(description="""Updates group""")
    async def update(
        self, info: strawberryA.types.Info, group: "GroupUpdateGQLModel"
    ) -> "GroupEditorGQLModel":
        async with withInfo(info) as session:
            lastchange = group.lastchange
            # print(lastchange)
            # updated = await resolveUpdateGroup(session,  id=self.id, data=group)
            loader = getLoader(info).groups
            updated = await resolveUpdateGroup(session, id=self.id, data=group)
            #updated = await loader.update(self, extraValues=data)
            # print(updated)
            # print(group.lastchange)
            # print(updated.lastchange)
            if lastchange == group.lastchange:
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = GroupEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result

    @strawberryA.field(description="""Create user and DO NOT introduce membership""")
    async def create_user(
        self, info: strawberryA.types.Info, user: "UserInsertGQLModel"
    ) -> "UserGQLModel":
        # session = AsyncSessionFromInfo(info)
        async with withInfo(info) as session:
            print("create_user")
            newUser = await resolveInsertUser(session, user, {})
            await session.commit()
            print(newUser)
            # result = await resolveInsertMembership(session, None,
            #    extraAttributes={'user_id': newUser.id, 'group_id': self.id})
        result = await UserGQLModel.resolve_reference(info, newUser.id)
        return result


from gql_ug.GraphResolvers import resolveGroupForGroupType
from gql_ug.GraphResolvers import resolveGroupTypeById


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a group type (like Faculty)"""
)
class GroupTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        # result = await resolveGroupTypeById(session,  id)
        async with withInfo(info) as session:
            result = await resolveGroupTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""""")
    def lastchange(self) -> strawberryA.ID:
        return self.lastchange

    @strawberryA.field(description="""Group type name CZ""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Group type name EN""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""List of groups which have this type""")
    async def groups(
        self, info: strawberryA.types.Info
    ) -> typing.List["GroupGQLModel"]:
        # result = await resolveGroupForGroupType(session,  self.id)
        async with withInfo(info) as session:
            result = await resolveGroupForGroupType(session, self.id)
            return result


from gql_ug.GraphResolvers import resolveRoleForRoleType
from gql_ug.GraphResolvers import resolveRoleTypeById


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a role type (like Dean)"""
)
class RoleTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        # result = await resolveRoleTypeById(session,  id)
        async with withInfo(info) as session:
            result = await resolveRoleTypeById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Datetime stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Role type name CZ""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Role type name EN""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""List of roles with this type""")
    async def roles(self, info: strawberryA.types.Info) -> typing.List["RoleGQLModel"]:
        # result = await resolveRoleForRoleType(session,  self.id)
        async with withInfo(info) as session:
            result = await resolveRoleForRoleType(session, self.id)
            return result


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a role type (like Dean)"""
)
class RoleCategoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoader(info).rolecategories
        result = await loader.load(id)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Primary key""")
    def lastchange(self) -> strawberryA.ID:
        return self.lastchange

    @strawberryA.field(description="""Role type name CZ""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Role type name EN""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""List of roles with this type""")
    async def role_types(self, info: strawberryA.types.Info) -> typing.List["RoleTypeGQLModel"]:
        # result = await resolveRoleForRoleType(session,  self.id)
        loader = getLoader(info).roletypes
        rows = await loader.filter_by(category_id=self.id)
        return rows

from gql_ug.GraphResolvers import resolveRoleTypeById, resolverRoleById


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a role of a user in a group (like user A in group B is Dean)""",
)
class RoleGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        # result = await resolverRoleById(session,  id)
        loader = getLoader(info).roles
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result
        # async with withInfo(info) as session:
        #     result = await resolverRoleById(session, id)
        #     result._type_definition = cls._type_definition # little hack :)
        #     return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Time stamp""")
    def lastchange(self) -> strawberryA.ID:
        return self.lastchange

    @strawberryA.field(description="""If an user has still this role""")
    def valid(self) -> bool:
        return self.valid

    @strawberryA.field(description="""When an user has got this role""")
    def startdate(self) -> Union[str, None]:
        return self.startdate

    @strawberryA.field(description="""When an user has been removed from this role""")
    def enddate(self) -> Union[str, None]:
        return self.enddate

    @strawberryA.field(description="""Role type (like Dean)""")
    async def roletype(self, info: strawberryA.types.Info) -> RoleTypeGQLModel:
        # result = await resolveRoleTypeById(session,  self.roletype_id)
        result = await RoleTypeGQLModel.resolve_reference(info, self.roletype_id)
        return result

    @strawberryA.field(
        description="""User having this role. Must be member of group?"""
    )
    async def user(self, info: strawberryA.types.Info) -> UserGQLModel:
        # result = await resolveUserById(session,  self.user_id)
        result = await UserGQLModel.resolve_reference(info, self.user_id)
        return result

    @strawberryA.field(description="""Group where user has a role name""")
    async def group(self, info: strawberryA.types.Info) -> GroupGQLModel:
        # result = await resolveGroupById(session,  self.group_id)
        result = await GroupGQLModel.resolve_reference(info, self.group_id)
        return result


from gql_ug.GraphResolvers import (
    resolveUserById,
    resolveUserAll,
    resolveUserByRoleTypeAndGroup,
)
from gql_ug.GraphResolvers import (
    resolveGroupById,
    resolveGroupTypeById,
    resolveGroupAll,
    resolveGroupTypeAll,
)
from gql_ug.GraphResolvers import (
    resolveAllRoleTypes,
    resolveRoleTypeAll,
    resolveRoleTypeById,
)
from gql_ug.GraphResolvers import (
    resolveUsersByThreeLetters,
    resolveGroupsByThreeLetters,
)

from gql_ug.GraphResolvers import import_ug, export_ug
from gql_ug.GraphResolvers import userSelect, groupSelect, selectGroup, selectGroupType

from gql_ug.DBFeeder import randomDataStructure, createUniversity


@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Returns a list of users (paged)""")
    async def user_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[UserGQLModel]:
        # result = await resolveUserAll(session,  skip, limit)
        result = await getLoader(info).users.execute_select(
            userSelect.offset(skip).limit(limit)
        )
        return result
        # async with withInfo(info) as session:
        #     result = await resolveUserAll(session, skip, limit)
        #     return result

    @strawberryA.field(description="""Finds an user by their id""")
    async def user_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[UserGQLModel, None]:
        # result = await resolveUserById(session,  id)
        result = await UserGQLModel.resolve_reference(info=info, id=id)
        return result
        # async with withInfo(info) as session:
        #     result = await resolveUserById(session, id)
        #     return result

    @strawberryA.field(
        description="""Finds an user by letters in name and surname, letters should be atleast three"""
    )
    async def user_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[UserGQLModel]:
        # result = await resolveUsersByThreeLetters(session,  validity, letters)
        async with withInfo(info) as session:
            result = await resolveUsersByThreeLetters(session, validity, letters)
            return result

    @strawberryA.field(description="""Finds an users who plays in a group a roletype""")
    async def users_by_group_and_role_type(
        self,
        info: strawberryA.types.Info,
        group_id: strawberryA.ID,
        role_type_id: strawberryA.ID,
    ) -> List[UserGQLModel]:
        # result = await resolveUserByRoleTypeAndGroup(session,  group_id, role_type_id)

        async with withInfo(info) as session:
            result = await resolveUserByRoleTypeAndGroup(
                session, group_id, role_type_id
            )
            return result

    @strawberryA.field(description="""Returns a list of groups (paged)""")
    async def group_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[GroupGQLModel]:
        # result = await resolveGroupAll(session,  skip, limit)
        result = await getLoader(info).groups.execute_select(
            groupSelect.offset(skip).limit(limit)
        )
        return result
        # async with withInfo(info) as session:
        #     result = await resolveGroupAll(session, skip, limit)
        #     return result

    @strawberryA.field(description="""Finds a group by its id""")
    async def group_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[GroupGQLModel, None]:
        # result = await resolveGroupById(session,  id)
        result = await GroupGQLModel.resolve_reference(info=info, id=id)
        return result
        # async with withInfo(info) as session:
        #     result = await resolveGroupById(session, id)
        #     return result

    @strawberryA.field(
        description="""Finds an user by letters in name and surname, letters should be atleast three"""
    )
    async def group_by_letters(
        self,
        info: strawberryA.types.Info,
        validity: Union[bool, None] = None,
        letters: str = "",
    ) -> List[GroupGQLModel]:
        # result = await resolveGroupsByThreeLetters(session,  validity, letters)
        async with withInfo(info) as session:
            result = await resolveGroupsByThreeLetters(session, validity, letters)
            return result

    @strawberryA.field(description="""Returns a list of groups types (paged)""")
    async def group_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 20
    ) -> List[GroupTypeGQLModel]:
        loader = getLoader(info).grouptypes
        result = await loader.execute_select(selectGroupType.offset(skip).limit(limit))
        return result

    @strawberryA.field(description="""Finds a group type by its id""")
    async def group_type_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[GroupTypeGQLModel, None]:
        # result = await resolveGroupTypeById(session,  id)
        result = await GroupTypeGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds all roles types paged""")
    async def role_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[RoleTypeGQLModel]:
        # result = await resolveRoleTypeAll(session,  skip, limit)
        async with withInfo(info) as session:
            result = await resolveRoleTypeAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Finds a role type by its id""")
    async def role_type_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[RoleTypeGQLModel, None]:
        result = await RoleTypeGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds a role type by its id""")
    async def role_category_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[RoleCategoryGQLModel, None]:
        result = await RoleCategoryGQLModel.resolve_reference(info,  id)
        return result

    @strawberryA.field(description="""Random university""")
    async def randomUniversity(
        self, name: str, info: strawberryA.types.Info
    ) -> GroupGQLModel:
        async with withInfo(info) as session:
            # newId = await randomDataStructure(session,  name)
            newId = await randomDataStructure(session, name)
            print("random university id", newId)
            # result = await resolveGroupById(session,  newId)
            result = await resolveGroupById(session, newId)
            print("db response", result.name)
            return result

    @strawberryA.field(description="""exports ug related data into inner file""")
    async def export_ug(self, info: strawberryA.types.Info) -> "str":
        async with withInfo(info) as session:
            # result = await export_ug(AsyncSessionFromInfo(info))
            result = await export_ug(session)
            return result

    @strawberryA.field(description="""imports ug related data from inner file""")
    async def import_ug(self, info: strawberryA.types.Info) -> "str":
        print("import_ug started")
        asyncSessionMaker = info.context["asyncSessionMaker"]
        result = await import_ug(asyncSessionMaker)
        print("import_ug returned")
        return result

    # @strawberryA.field(description="""returns a object for new inserts""")
    # async def insert(self, info: strawberryA.types.Info) -> UGInsertGQLModel:
    #     return await UGInsertGQLModel.resolve_reference(info)
    
###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

@strawberryA.input
class UserUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime  # razitko
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    valid: Optional[bool] = None

@strawberryA.input
class UserInsertGQLModel:
    id: Optional[strawberryA.ID] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    valid: Optional[bool] = None

@strawberryA.type
class UserResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def user(self, info: strawberryA.types.Info) -> Union[UserGQLModel, None]:
        result = await UserGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class GroupUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    grouptype_id: Optional[strawberryA.ID] = None
    mastergroup_id: Optional[strawberryA.ID] = None
    valid: Optional[bool] = None


@strawberryA.input
class GroupInsertGQLModel:
    name: str
    id: Optional[strawberryA.ID] = None
    grouptype_id: Optional[strawberryA.ID] = None
    mastergroup_id: Optional[strawberryA.ID] = None
    valid: Optional[bool] = None

@strawberryA.type
class GroupResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of group operation""")
    async def group(self, info: strawberryA.types.Info) -> Union[GroupGQLModel, None]:
        print("GroupResultGQLModel", "group", self.id, flush=True)
        result = await GroupGQLModel.resolve_reference(info, self.id)
        print("GroupResultGQLModel", result.id, result.name, flush=True)
        return result

@strawberryA.input
class MembershipUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime   
    valid: Optional[bool] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None

@strawberryA.input
class MembershipInsertGQLModel:
    user_id: strawberryA.ID
    group_id: strawberryA.ID
    id: Optional[strawberryA.ID] = None
    valid: Optional[bool] = True
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None

@strawberryA.type
class MembershipResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of membership operation""")
    async def membership(self, info: strawberryA.types.Info) -> Union[MembershipGQLModel, None]:
        result = await MembershipGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.input
class GeneralTypeUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberryA.input
class GeneralTypeInsertGQLModel:
    id: Optional[strawberryA.ID] = None
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberryA.type
class GroupTypeResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of grouptype operation""")
    async def group_type(self, info: strawberryA.types.Info) -> Union[GroupTypeGQLModel, None]:
        result = await GroupTypeGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.type
class RoleTypeResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of role type operation""")
    async def role_type(self, info: strawberryA.types.Info) -> Union[RoleTypeGQLModel, None]:
        result = await RoleTypeGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.type
class RoleCategoryResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of role category operation""")
    async def role_category(self, info: strawberryA.types.Info) -> Union[RoleCategoryGQLModel, None]:
        result = await RoleCategoryGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class RoleUpdateGQLModel:
    id: strawberryA.ID
    lastchange: datetime.datetime
    valid: Optional[bool] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None

@strawberryA.input
class RoleInsertGQLModel:
    user_id: strawberryA.ID
    group_id: strawberryA.ID
    roletype_id: strawberryA.ID
    id: Optional[strawberryA.ID] = None
    valid: Optional[bool] = True
    startdate: Optional[datetime.datetime] = datetime.datetime.now()
    enddate: Optional[datetime.datetime] = None

@strawberryA.type
class RoleResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def role(self, info: strawberryA.types.Info) -> Union[RoleGQLModel, None]:
        result = await RoleGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberryA.type
class Mutation:

    @strawberryA.mutation(description="""Update the membership, cannot update group / user""")
    async def membership_update(self, 
        info: strawberryA.types.Info, 
        membership: "MembershipUpdateGQLModel"
    ) -> "MembershipResultGQLModel":

        loader = getLoader(info).memberships
        updatedrow = await loader.update(membership)

        result = MembershipResultGQLModel()
        result.msg = "ok"
        result.id = membership.id

        if updatedrow is None:
            result.msg = "fail"
       
        return result


    @strawberryA.mutation(description="""Inserts new membership""")
    async def membership_insert(self, 
        info: strawberryA.types.Info, 
        membership: "MembershipInsertGQLModel"
    ) -> "MembershipResultGQLModel":

        loader = getLoader(info).memberships
        row = await loader.insert(membership)

        result = MembershipResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        
        return result


    @strawberryA.mutation
    async def user_update(self, info: strawberryA.types.Info, user: UserUpdateGQLModel) -> UserResultGQLModel:
        #print("user_update", flush=True)
        #print(user, flush=True)
        loader = getLoader(info).users
        
        updatedrow = await loader.update(user)
        #print("user_update", updatedrow, flush=True)
        result = UserResultGQLModel()
        result.id = user.id

        if updatedrow is None:
            result.msg = "fail"
        else:
            result.msg = "ok"
        print("user_update", result.msg, flush=True)
        return result

    @strawberryA.mutation
    async def user_insert(self, info: strawberryA.types.Info, user: UserInsertGQLModel) -> UserResultGQLModel:
        loader = getLoader(info).users
        
        row = await loader.insert(user)

        result = UserResultGQLModel()
        result.id = row.id
        result.msg = "ok"
        
        return result

    @strawberryA.mutation(description="""
        Allows a update of group, also it allows to change the mastergroup of the group
    """)
    async def group_update(self, info: strawberryA.types.Info, group: GroupUpdateGQLModel) -> GroupResultGQLModel:
        loader = getLoader(info).groups
        
        updatedrow = await loader.update(group)
        #print(updatedrow, updatedrow.id, updatedrow.name, flush=True)
        if updatedrow is None:
            return GroupResultGQLModel(id=group.id, msg="fail")
        else:
            return GroupResultGQLModel(id=group.id, msg="ok")
        

    @strawberryA.mutation(description="""
        Allows a update of group, also it allows to change the mastergroup of the group
    """)
    async def group_insert(self, info: strawberryA.types.Info, group: GroupInsertGQLModel) -> GroupResultGQLModel:
        loader = getLoader(info).groups
        
        updatedrow = await loader.insert(group)
        print("group_insert", updatedrow, updatedrow.id, updatedrow.name, flush=True)
        result = GroupResultGQLModel()
        result.id = updatedrow.id
        result.msg = "ok"

        if updatedrow is None:
            result.msg = "fail"
        
        return result

    @strawberryA.mutation(description="""
        Allows a update of group, also it allows to change the mastergroup of the group
    """)
    async def group_type_update(self, info: strawberryA.types.Info, group_type: GeneralTypeUpdateGQLModel) -> GroupTypeResultGQLModel:
        loader = getLoader(info).grouptypes
        
        updatedrow = await loader.update(group_type)
        result = GroupTypeResultGQLModel()
        result.msg = "ok"
        result.id = group_type.id
        if updatedrow is None:
            result.msg = "fail"
        
        return result

    @strawberryA.mutation(description="""
        Inserts a group
    """)
    async def group_type_insert(self, info: strawberryA.types.Info, group_type: GeneralTypeInsertGQLModel) -> GroupTypeResultGQLModel:
        loader = getLoader(info).grouptypes
        
        updatedrow = await loader.insert(group_type)
        result = GroupTypeResultGQLModel()
        result.id = updatedrow.id
        result.msg = "ok"

        if updatedrow is None:
            result.msg = "fail"
        
        return result

    @strawberryA.mutation(description="""
        Allows to assign the group to8 specified master group
    """)
    async def group_update_master(self, 
        info: strawberryA.types.Info, 
        master_id: strawberryA.ID,
        group: GroupUpdateGQLModel) -> GroupResultGQLModel:
        loader = getLoader(info).groups
        
        result = GroupResultGQLModel()
        result.id = group.id
        result.msg = "ok"

        #use asyncio.gather here
        updatedrow = await loader.load(group.id)
        if updatedrow is None:
            result.msg = "fail"
            return result

        masterrow = await loader.load(master_id)
        if masterrow is None:
            result.msg = "fail"
            return result

        updatedrow.master_id = master_id
        updatedrow = await loader.update(updatedrow)
        
        if updatedrow is None:
            result.msg = "fail"
        
        return result


    @strawberryA.mutation(description="""Updates a role""")
    async def role_update(self, 
        info: strawberryA.types.Info, 
        role: RoleUpdateGQLModel
    ) -> RoleResultGQLModel:

        loader = getLoader(info).roles
        updatedrow = await loader.update(role)

        result = RoleResultGQLModel()
        result.msg = "ok"
        result.id = role.id
        
        if updatedrow is None:
            result.msg = "fail"        
        
        return result

    @strawberryA.mutation(description="""Inserts a role""")
    async def role_insert(self, 
        info: strawberryA.types.Info, 
        role: RoleInsertGQLModel
    ) -> RoleResultGQLModel:

        loader = getLoader(info).roles

        result = RoleResultGQLModel()
        result.msg = "ok"
        
        updatedrow = await loader.insert(role)
        result.id = updatedrow.id
        
        return result

    @strawberryA.mutation(description="""Updates existing roleType record""")
    async def role_type_update(self, 
        info: strawberryA.types.Info, 
        role_type: GeneralTypeUpdateGQLModel

    ) -> RoleTypeResultGQLModel:
        print("role_type_update", role_type, flush=True)
        loader = getLoader(info).roletypes
        row = await loader.update(role_type)
        if row is not None:
            print("role_type_update", row, row.name, row.id, flush=True)
        result = RoleTypeResultGQLModel()
        result.msg = "ok"
        result.id = role_type.id
        if row is None:
            result.msg = "fail"
        
        return result

    @strawberryA.mutation(description="""Inserts a new roleType record""")
    async def role_type_insert(self, 
        info: strawberryA.types.Info, 
        role_type: GeneralTypeInsertGQLModel

    ) -> RoleTypeResultGQLModel:
        #print("role_type_update", role_type, flush=True)
        loader = getLoader(info).roletypes
        row = await loader.insert(role_type)
        if row is not None:
            print("role_type_update", row, row.name, row.id, flush=True)
        result = RoleTypeResultGQLModel()
        result.msg = "ok"
        result.id = row.id       
        return result

    @strawberryA.mutation(description="""Updates a role category""")
    async def role_category_update(self, 
        info: strawberryA.types.Info, 
        role_category: GeneralTypeUpdateGQLModel

    ) -> RoleCategoryResultGQLModel:

        loader = getLoader(info).rolecategories
        row = await loader.update(role_category)

        result = RoleCategoryResultGQLModel()
        result.msg = "ok"
        result.id = role_category.id
        if row is None:
            result.msg = "fail"
        else:
            result.id = row.id

        
        return result
    
    @strawberryA.mutation(description="""Inserts a role category""")
    async def role_category_insert(self, 
        info: strawberryA.types.Info, 
        role_category: GeneralTypeInsertGQLModel

    ) -> RoleCategoryResultGQLModel:

        loader = getLoader(info).rolecategories
        row = await loader.insert(role_category)

        result = RoleCategoryResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        
        return result

    
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(query=Query, types=(UserGQLModel,), mutation=Mutation)
