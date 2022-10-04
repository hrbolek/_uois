from pydoc import resolve
from typing import List, Union
import typing
import strawberry as strawberryA
import uuid

def AsyncSessionFromInfo(info):
    return info.context['session']



@strawberryA.federation.type(keys=["id"], description="""Entity representing a relation between an user and a group""")
class MembershipGQLModel:
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""user""")
    async def user(self) -> 'UserGQLModel':
        return self.user

    @strawberryA.field(description="""group""")
    async def group(self) -> 'GroupGQLModel':
        return self.group

    @strawberryA.field(description="""is the membership is still valid""")
    async def valid(self) -> bool:
        return self.valid

    @strawberryA.field(description="""date when the membership begins""")
    async def startdate(self) -> bool:
        return self.startdate

    @strawberryA.field(description="""date when the membership ends""")
    async def enddate(self) -> bool:
        return self.enddate

from gql_ug.GraphResolvers import resolveMembershipForUser, resolveRolesForUser
@strawberryA.federation.type(keys=["id"], description="""Entity representing a user""")
class UserGQLModel:

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
    def email(self) -> str:
        return self.email

    @strawberryA.field(description="""List of groups, where the user is member""")
    async def membership(self, info: strawberryA.types.Info) -> typing.List['MembershipGQLModel']:
        result = await resolveMembershipForUser(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(description="""List of groups, where the user is member""")
    async def roles(self, info: strawberryA.types.Info) -> typing.List['RoleGQLModel']:
        result = await resolveRolesForUser(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(description="""List of groups given type, where the user is member""")
    async def member_of(self, grouptype_id: uuid.UUID, info: strawberryA.types.Info) -> typing.List['GroupGQLModel']:
        """type hinting pouziva strawberry ke spravne deserializaci, vysledek deserializace ma vliv na operatory (napr. __EQ__)
           v tomto pripade je mozne primo srovnavat, pokud by jako hint typ u grouptype_id byl str, muselo by se srovnavat jinak
        """
        memberships = await resolveMembershipForUser(AsyncSessionFromInfo(info), self.id)
        #memberships = [ membership for membership in memberships ]
        #print('member_of', memberships)
        #result = [ membership.group.name for membership in memberships ]
        #print('member_of 2', result)
        #result = [ membership.group.grouptype_id for membership in memberships ]
        #print('member_of 2b', result)
        result = [
            membership.group 
                for membership in memberships 
                    #if f'{membership.group.grouptype_id}' == grouptype_id
                    if membership.group.grouptype_id == grouptype_id
        ]
        #print('member_of 3', result)
        #result = [ membership.group for membership in memberships ]
        #print('member_of 4', result)
        return result

    @strawberryA.field(description="""returns the user editor if possible""")
    async def editor(self, info: strawberryA.types.Info) -> Union['UserEditorGQLModel', None]:
        ## current user must be checked if has rights to get the editor
        ## if not, then None value must be returned
        return self

@strawberryA.input
class UserUpdateGQLModel:
    name: str = None
    surname: str = None
    email: str = None
    valid: bool = None

from gql_ug.GraphResolvers import resolverUpdateUser
@strawberryA.federation.type(keys=["id"], description="""Entity representing an editable user""")
class UserEditorGQLModel:
    ##
    ## Mutace, obejiti problemu s federativnim API
    ##
    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Updates the user data""")
    async def update(self, info: strawberryA.types.Info, data: UserUpdateGQLModel) -> UserGQLModel:
        result = await resolverUpdateUser(AsyncSessionFromInfo(info), id=self.id, data=data)
        return result

    pass


from gql_ug.GraphResolvers import resolveMembershipForGroup, resolveMastergroupForGroup, resolveSubgroupsForGroup, resolveRolesForGroup
from gql_ug.GraphPermissions import GroupEditorPermission
@strawberryA.federation.type(keys=["id"], description="""Entity representing a group""")
class GroupGQLModel:

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Group's name (like Department of Intelligent Control)""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Group's type (like Department)""")
    def grouptype(self, info: strawberryA.types.Info) -> Union['GroupTypeGQLModel', None]:
        if self.grouptype_id is None:
            return None
        else:
            result = resolveGroupTypeById(AsyncSessionFromInfo(info), self.grouptype_id)
            return result

    @strawberryA.field(description="""Directly commanded groups""")
    async def subgroups(self, info: strawberryA.types.Info) -> typing.List['GroupGQLModel']:
        result = await resolveSubgroupsForGroup(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(description="""Commanding group""")
    async def mastergroup(self, info: strawberryA.types.Info) -> typing.Union['GroupGQLModel', None]:
        if self.mastergroup_id is None:
            return None
        else:
            result = await resolveMastergroupForGroup(AsyncSessionFromInfo(info), self.mastergroup_id)
            return result

    @strawberryA.field(description="""List of users who are member of the group""")
    async def memberships(self, info: strawberryA.types.Info) -> typing.List['MembershipGQLModel']:
        result = await resolveMembershipForGroup(AsyncSessionFromInfo(info), self.id)
        return result       

    @strawberryA.field(description="""List of roles in the group""")
    async def roles(self, info: strawberryA.types.Info) -> typing.List['RoleGQLModel']:
        result = await resolveRolesForGroup(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(
        permission_classes=[GroupEditorPermission],
        description="""List of roles in the group""")
    async def editor(self, info: strawberryA.types.Info) -> Union['GroupGQLEditorModel', None]:
        # check if user has right to get editor (can edit this group)
        # if hasNoRight:
        #    return None
        # else:
        return self

@strawberryA.input
class GroupUpdateGQLModel:
    name: str = None
    type_id: uuid.UUID = None
    valid: bool = None

from gql_ug.GraphResolvers import resolveUpdateGroup, resolverRoleById, resolveInsertRole, resolveInsertMembership, resolveMembershipById
@strawberryA.federation.type(keys=["id"], description="""Entity representing an editable group""")
class GroupGQLEditorModel:
    ##
    ## Mutace, obejiti problemu s federativnim API
    ##
    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Create a new membership""")
    async def add_membership(self, info: strawberryA.types.Info, user_id: uuid.UUID) -> 'MembershipGQLModel':
        result = await resolveInsertMembership(AsyncSessionFromInfo(info), None, 
            extraAttributes={'user_id': user_id, 'group_id': self.id})
        return result

    @strawberryA.field(description="""Invalidate a new membership""")
    async def invalidate_membership(self, info: strawberryA.types.Info, membership_id: uuid.UUID) -> 'MembershipGQLModel':
        session = AsyncSessionFromInfo(info)
        role = await resolveMembershipById(session, membership_id)
        role.valid = False
        await session.commit()
        return role

    @strawberryA.field(description="""Create a new role""")
    async def add_role(self, info: strawberryA.types.Info, user_id: uuid.UUID, roletype_id: uuid.UUID) -> 'RoleGQLModel':
        result = await resolveInsertRole(AsyncSessionFromInfo(info), None, 
            extraAttributes={'user_id': user_id, 'group_id': self.id, 'roletype_id': roletype_id})
        return result

    @strawberryA.field(description="""Invalidate a new role""")
    async def invalidate_role(self, info: strawberryA.types.Info, role_id: uuid.UUID) -> 'RoleGQLModel':
        session = AsyncSessionFromInfo(info)
        role = await resolverRoleById(session, role_id)
        role.valid = False
        await session.commit()
        return role

    @strawberryA.field(description="""Create a new role""")
    async def create_subgroup(self, info: strawberryA.types.Info, grouptype_id: uuid.UUID) -> 'GroupGQLModel':
        pass

    @strawberryA.field(description="""Create a new role""")
    async def assign_subgroup(self, info: strawberryA.types.Info, subgroup_id: strawberryA.ID) -> 'GroupGQLModel':
        #updated = await resolveUpdateGroup(AsyncSessionFromInfo(info), subgroup_id, )
        pass

    @strawberryA.field(description="""Updates group""")
    async def update(self, info: strawberryA.types.Info, group: GroupUpdateGQLModel) -> 'GroupGQLModel':
        updated = await resolveUpdateGroup(AsyncSessionFromInfo(info), self.id, group)
        print(updated)
        return updated   

from gql_ug.GraphResolvers import resolveGroupForGroupType
@strawberryA.federation.type(keys=["id"], description="""Entity representing a group type (like Faculty)""")
class GroupTypeGQLModel:
    
    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Group type name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""List of groups which have this type""")
    async def groups(self, info: strawberryA.types.Info) -> typing.List['GroupGQLModel']:
        result = await resolveGroupForGroupType(AsyncSessionFromInfo(info), self.id)
        return result       

from gql_ug.GraphResolvers import resolveRoleForRoleType
@strawberryA.federation.type(keys=["id"], description="""Entity representing a role type (like Dean)""")
class RoleTypeGQLModel:

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Role type name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""List of roles with this type""")
    async def roles(self, info: strawberryA.types.Info) -> typing.List['RoleGQLModel']:
        result = await resolveRoleForRoleType(AsyncSessionFromInfo(info), self.id)
        return result



from gql_ug.GraphResolvers import resolveRoleTypeById
@strawberryA.federation.type(keys=["id"], description="""Entity representing a role of a user in a group (like user A in group B is Dean)""")
class RoleGQLModel:

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""If an user has still this role""")
    def valid(self) -> bool:
        return self.valid

    @strawberryA.field(description="""When an user has got this role""")
    def startdate(self) -> str:
        return self.startdate

    @strawberryA.field(description="""When an user has been removed from this role""")
    def enddate(self) -> str:
        return self.enddate

    @strawberryA.field(description="""Role type (like Dean)""")
    async def roletype(self, info: strawberryA.types.Info) -> RoleTypeGQLModel:
        result = await resolveRoleTypeById(AsyncSessionFromInfo(info), self.roletype_id)
        return result

    @strawberryA.field(description="""User having this role. Must be member of group?""")
    async def user(self, info: strawberryA.types.Info) -> UserGQLModel:
        result = await resolveUserById(AsyncSessionFromInfo(info), self.user_id)
        return result

    @strawberryA.field(description="""Group where user has a role name""")
    async def group(self, info: strawberryA.types.Info) -> GroupGQLModel:
        result = await resolveGroupById(AsyncSessionFromInfo(info), self.group_id)
        return result

from gql_ug.GraphResolvers import resolveUserById, resolveGroupById, resolveGroupTypeById
from gql_ug.GraphResolvers import resolveAllRoleTypes
from gql_ug.GraphResolvers import resolveUsersByThreeLetters, resolveGroupsByThreeLetters
from gql_ug.DBFeeder import randomDataStructure
@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an user by their id""")
    async def user_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[UserGQLModel, None]:
        result = await resolveUserById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(
        description="""Finds an user by letters in name and surname, letters should be atleast three""")
    async def user_by_letters(self, info: strawberryA.types.Info, validity: Union[bool, None] = None, letters: str = '') -> List[UserGQLModel]:
        print('user_by_letters')
        result = await resolveUsersByThreeLetters(AsyncSessionFromInfo(info), validity, letters)
        return result

    @strawberryA.field(description="""Finds a group by its id""")
    async def group_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[GroupGQLModel, None]:
        result = await resolveGroupById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Finds an user by letters in name and surname, letters should be atleast three""")
    async def group_by_letters(self, info: strawberryA.types.Info, validity: Union[bool, None] = None, letters: str = '') -> List[GroupGQLModel]:
        result = await resolveGroupsByThreeLetters(AsyncSessionFromInfo(info), validity, letters)
        return result

    @strawberryA.field(description="""Finds a group type by its id""")
    async def group_type_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[GroupTypeGQLModel, None]:
        result = await resolveGroupTypeById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Finds a group type by its id""")
    async def roletypes(self, info: strawberryA.types.Info) -> List[RoleTypeGQLModel]:
        result = await resolveAllRoleTypes(AsyncSessionFromInfo(info))
        return result

    @strawberryA.field(description="""Random university""")
    async def randomUniversity(self, name: str, info: strawberryA.types.Info) -> GroupGQLModel:
        newId = await randomDataStructure(AsyncSessionFromInfo(info), name)
        print('random university id', newId)
        result = await resolveGroupById(AsyncSessionFromInfo(info), newId)
        print('db response', result.name)
        return result
    