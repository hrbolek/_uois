import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import gql_ug.GraphTypeDefinitions

def getLoader(info):
    return info.context["all"]

GroupTypeGQLModel = Annotated["GroupTypeGQLModel", strawberry.lazy(".groupTypeGQLModel")]
MembershipGQLModel = Annotated["MembershipGQLModel", strawberry.lazy(".membershipGQLModel")]
RoleGQLModel = Annotated["RoleGQLModel", strawberry.lazy(".roleGQLModel")]

@strawberry.federation.type(keys=["id"], description="""Entity representing a group""")
class GroupGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        if id is None: return None
        loader = getLoader(info).groups
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(
        description="""Group's name (like Department of Intelligent Control)"""
    )
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Group's validity (still exists?)""")
    def valid(self) -> bool:
        if not self.valid:
            return False
        else:
            return self.valid

    @strawberry.field(description="""""")
    def lastchange(self) -> Union[datetime.datetime, None]:
        result = self.lastchange
        return result

    @strawberry.field(description="""Group's type (like Department)""")
    async def grouptype(
        self, info: strawberry.types.Info
    ) -> Union["GroupTypeGQLModel", None]:
        result = await gql_ug.GraphTypeDefinitions.GroupTypeGQLModel.resolve_reference(info, id=self.grouptype_id)
        return result

    @strawberry.field(description="""Directly commanded groups""")
    async def subgroups(
        self, info: strawberry.types.Info
    ) -> List["GroupGQLModel"]:
        loader = getLoader(info).groups
        print(self.id)
        result = await loader.filter_by(mastergroup_id=self.id)
        return result

    @strawberry.field(description="""Commanding group""")
    async def mastergroup(
        self, info: strawberry.types.Info
    ) -> Union["GroupGQLModel", None]:
        result = await GroupGQLModel.resolve_reference(info, id=self.mastergroup_id)
        return result

    @strawberry.field(description="""List of users who are member of the group""")
    async def memberships(
        self, info: strawberry.types.Info
    ) -> List["MembershipGQLModel"]:
        # result = await resolveMembershipForGroup(session,  self.id, skip, limit)
        # async with withInfo(info) as session:
        #     result = await resolveMembershipForGroup(session, self.id, skip, limit)
        #     return result

        loader = getLoader(info).memberships
        #print(self.id)
        result = await loader.filter_by(group_id=self.id)
        return result

    @strawberry.field(description="""List of roles in the group""")
    async def roles(self, info: strawberry.types.Info) -> List["RoleGQLModel"]:
        # result = await resolveRolesForGroup(session,  self.id)
        loader = getLoader(info).roles
        result = await loader.filter_by(group_id=self.id)
        return result

    # @strawberry.field(
    #     # permission_classes=[GroupEditorPermission],
    #     description="""List of roles in the group"""
    # )
    # async def editor(
    #     self, info: strawberry.types.Info
    # ) -> Union["GroupEditorGQLModel", None]:
    #     # check if user has right to get editor (can edit this group)
    #     # if hasNoRight:
    #     #    return None
    #     # else:
    #     return self

#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberry.field(description="""Returns a list of groups (paged)""")
async def group_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
) -> List[GroupGQLModel]:
    # result = await resolveGroupAll(session,  skip, limit)
    loader = getLoader(info).groups
    result = await loader.page(skip, limit)
    return result

@strawberry.field(description="""Finds a group by its id""")
async def group_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> Union[GroupGQLModel, None]:
    result = await GroupGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(
    description="""Finds an user by letters in name and surname, letters should be atleast three"""
)
async def group_by_letters(
    self,
    info: strawberry.types.Info,
    validity: Union[bool, None] = None,
    letters: str = "",
) -> List[GroupGQLModel]:
    # result = await resolveGroupsByThreeLetters(session,  validity, letters)
    loader = getLoader(info).groups

    if len(letters) < 3:
        return []
    stmt = loader.getSelectStatement()
    model = loader.getModel()
    stmt = stmt.where(model.name.like(f"%{letters}%"))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    result = await loader.execute_select(stmt)
    return result

# @strawberry.field(description="""Random university""")
# async def randomUniversity(
#     self, name: str, info: strawberry.types.Info
# ) -> GroupGQLModel:
#     async with withInfo(info) as session:
#         # newId = await randomDataStructure(session,  name)
#         newId = await randomDataStructure(session, name)
#         print("random university id", newId)
#         # result = await resolveGroupById(session,  newId)
#         result = await resolveGroupById(session, newId)
#         print("db response", result.name)
#         return result

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input
class GroupUpdateGQLModel:
    id: strawberry.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    grouptype_id: Optional[strawberry.ID] = None
    mastergroup_id: Optional[strawberry.ID] = None
    valid: Optional[bool] = None


@strawberry.input
class GroupInsertGQLModel:
    name: str
    id: Optional[strawberry.ID] = None
    grouptype_id: Optional[strawberry.ID] = None
    mastergroup_id: Optional[strawberry.ID] = None
    valid: Optional[bool] = None

@strawberry.type
class GroupResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of group operation""")
    async def group(self, info: strawberry.types.Info) -> Union[GroupGQLModel, None]:
        print("GroupResultGQLModel", "group", self.id, flush=True)
        result = await GroupGQLModel.resolve_reference(info, self.id)
        print("GroupResultGQLModel", result.id, result.name, flush=True)
        return result

@strawberry.mutation(description="""
    Allows a update of group, also it allows to change the mastergroup of the group
""")
async def group_update(self, info: strawberry.types.Info, group: GroupUpdateGQLModel) -> GroupResultGQLModel:
    loader = getLoader(info).groups
    
    updatedrow = await loader.update(group)
    #print(updatedrow, updatedrow.id, updatedrow.name, flush=True)
    if updatedrow is None:
        return GroupResultGQLModel(id=group.id, msg="fail")
    else:
        return GroupResultGQLModel(id=group.id, msg="ok")
    

@strawberry.mutation(description="""
    Allows a update of group, also it allows to change the mastergroup of the group
""")
async def group_insert(self, info: strawberry.types.Info, group: GroupInsertGQLModel) -> GroupResultGQLModel:
    loader = getLoader(info).groups
    
    updatedrow = await loader.insert(group)
    print("group_insert", updatedrow, updatedrow.id, updatedrow.name, flush=True)
    result = GroupResultGQLModel()
    result.id = updatedrow.id
    result.msg = "ok"

    if updatedrow is None:
        result.msg = "fail"
    
    return result

@strawberry.mutation(description="""
        Allows to assign the group to8 specified master group
    """)
async def group_update_master(self, 
    info: strawberry.types.Info, 
    master_id: strawberry.ID,
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