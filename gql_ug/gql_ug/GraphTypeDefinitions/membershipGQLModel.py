import datetime
import strawberry
from typing import List, Optional, Union, Annotated
import gql_ug.GraphTypeDefinitions

def getLoader(info):
    return info.context["all"]

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".groupGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".userGQLModel")]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a group""",
)
class MembershipGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        if id is None: return None
        loader = getLoader(info).memberships
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
            result.__strawberry_definition__ = cls._type_definition # some version of strawberry changed :(
        return result

    @strawberry.field(description="""primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""time stamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""user""")
    async def user(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        # return self.user
        result = await gql_ug.GraphTypeDefinitions.UserGQLModel.resolve_reference(info=info, id=self.user_id)
        return result

    @strawberry.field(description="""group""")
    async def group(self, info: strawberry.types.Info) -> Optional["GroupGQLModel"]:
        # return self.group
        result = await gql_ug.GraphTypeDefinitions.GroupGQLModel.resolve_reference(info=info, id=self.group_id)
        return result

    @strawberry.field(description="""is the membership is still valid""")
    async def valid(self) -> Union[bool, None]:
        return self.valid

    @strawberry.field(description="""date when the membership begins""")
    async def startdate(self) -> Union[datetime.datetime, None]:
        return self.startdate

    @strawberry.field(description="""date when the membership ends""")
    async def enddate(self) -> Union[datetime.datetime, None]:
        return self.enddate

#####################################################################
#
# Special fields for query
#
#####################################################################

#####################################################################
#
# Mutation section
#
#####################################################################
import datetime

@strawberry.input
class MembershipUpdateGQLModel:
    id: strawberry.ID
    lastchange: datetime.datetime   
    valid: Optional[bool] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None

@strawberry.input
class MembershipInsertGQLModel:
    user_id: strawberry.ID
    group_id: strawberry.ID
    id: Optional[strawberry.ID] = None
    valid: Optional[bool] = True
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None

@strawberry.type
class MembershipResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of membership operation""")
    async def membership(self, info: strawberry.types.Info) -> Union[MembershipGQLModel, None]:
        result = await MembershipGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(description="""Update the membership, cannot update group / user""")
async def membership_update(self, 
    info: strawberry.types.Info, 
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


@strawberry.mutation(description="""Inserts new membership""")
async def membership_insert(self, 
    info: strawberry.types.Info, 
    membership: "MembershipInsertGQLModel"
) -> "MembershipResultGQLModel":

    loader = getLoader(info).memberships
    row = await loader.insert(membership)

    result = MembershipResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    
    return result