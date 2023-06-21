import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import gql_ug.GraphTypeDefinitions


def getLoader(info):
    return info.context["all"]

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a group type (like Faculty)"""
)
class GroupTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoader(info).grouptypes
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(
            return result
        
    @strawberry.field(description="""Primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""""")
    def lastchange(self) -> strawberry.ID:
        return self.lastchange

    @strawberry.field(description="""Group type name CZ""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Group type name EN""")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""List of groups which have this type""")
    async def groups(
        self, info: strawberry.types.Info
    ) -> List["GroupGQLModel"]:
        # result = await resolveGroupForGroupType(session,  self.id)
        loader = getLoader(info).groups
        result = await loader.filter_by(grouptype_id=self.id)
        return result

#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberry.field(description="""Returns a list of groups types (paged)""")
async def group_type_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 20
) -> List[GroupTypeGQLModel]:
    loader = getLoader(info).grouptypes
    result = await loader.page(skip, limit)
    return result

@strawberry.field(description="""Finds a group type by its id""")
async def group_type_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> Union[GroupTypeGQLModel, None]:
    # result = await resolveGroupTypeById(session,  id)
    result = await GroupTypeGQLModel.resolve_reference(info, id)
    return result

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input
class GroupTypeUpdateGQLModel:
    id: strawberry.ID
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberry.input
class GroupTypeInsertGQLModel:
    id: Optional[strawberry.ID] = None
    name: Optional[str] = None
    name_en: Optional[str] = None

@strawberry.type
class GroupTypeResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of grouptype operation""")
    async def group_type(self, info: strawberry.types.Info) -> Union[GroupTypeGQLModel, None]:
        result = await GroupTypeGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(description="""
        Allows a update of group, also it allows to change the mastergroup of the group
    """)
async def group_type_update(self, info: strawberry.types.Info, group_type: GroupTypeUpdateGQLModel) -> GroupTypeResultGQLModel:
    loader = getLoader(info).grouptypes
    
    updatedrow = await loader.update(group_type)
    result = GroupTypeResultGQLModel()
    result.msg = "ok"
    result.id = group_type.id
    if updatedrow is None:
        result.msg = "fail"
    
    return result

@strawberry.mutation(description="""
    Inserts a group
""")
async def group_type_insert(self, info: strawberry.types.Info, group_type: GroupTypeInsertGQLModel) -> GroupTypeResultGQLModel:
    loader = getLoader(info).grouptypes
    
    updatedrow = await loader.insert(group_type)
    result = GroupTypeResultGQLModel()
    result.id = updatedrow.id
    result.msg = "ok"

    if updatedrow is None:
        result.msg = "fail"
    
    return result    