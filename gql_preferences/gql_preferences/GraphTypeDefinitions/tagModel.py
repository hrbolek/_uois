import strawberry
from strawberry import lazy
import datetime
from typing import Union, Optional, List, TYPE_CHECKING, Annotated

def getLoaders(info):
    return info.context["all"]

def getUser(info):
    return info.context["user"]

PreferenceTagEntityGQLModel = Annotated["PreferenceTagEntityGQLModel", lazy(".tagEntityModel")]
UserGQLModel = Annotated["UserGQLModel", lazy(".externals")]
#from gql_preferences.GraphTypeDefinitions.tagEntityModel import PreferenceTagEntity as PreferenceTagEntityExecutor

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a tag""",
)
class PreferenceTagGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        if id is None:
            return None
        loader = getLoaders(info).tags
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="""primary key""")
    async def id(self, info: strawberry.types.Info) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""time stamp""")
    async def lastchange(self, info: strawberry.types.Info) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""date of creation""")
    async def created(self, info: strawberry.types.Info) -> datetime.datetime:
        return self.created

    @strawberry.field(description="""user who created this tag""")
    async def created_by(self, info: strawberry.types.Info) -> Union[UserGQLModel, None]:
        result = await UserGQLModel.resolve_reference(info=info, id=self.createdby)
        return result

    @strawberry.field(description="""user who updated this tag""")
    async def changed_by(self, info: strawberry.types.Info) -> Union[UserGQLModel, None]:
        result = await UserGQLModel.resolve_reference(info=info, id=self.changedby)
        return result

    @strawberry.field(description="""tag value, can be "red", "2023", etc. """)
    async def name(self, info: strawberry.types.Info) -> Union[str, None]:
        return self.name

    @strawberry.field(description="""tag value, can be "red", "2023", etc. """)
    async def links(self, info: strawberry.types.Info) -> List["PreferenceTagEntityGQLModel"]:
        loader = getLoaders(info).tagentities
        result = await loader.filter_by(tag_id=self.id)
        return result



#####################################################################
#
# Special fields for query
#
#####################################################################

tags_description = """Returns list of tags associated with asking user."""
@strawberry.field(description=tags_description)
async def preference_tags(info: strawberry.types.Info) -> List["PreferenceTagGQLModel"]:
    actingUser = getUser(info)
    # print(actingUser)
    loader = getLoaders(info).tags
    result = await loader.filter_by(author_id=actingUser["id"])
    
    # result = list(result)
    # print(result)
    return result


#####################################################################
#
# Mutation section
#
#####################################################################

import datetime

@strawberry.input(description="""""")
class TagInsertGQLModel:
    name: str
    id: Optional[strawberry.ID] = None
    createdby: strawberry.Private[strawberry.ID] = None
    author_id: strawberry.Private[strawberry.ID] = None

@strawberry.input(description="""""")
class TagUpdateGQLModel:
    id: strawberry.ID
    name: str
    lastchange: datetime.datetime
    updatedby: strawberry.Private[strawberry.ID] = None

@strawberry.input(description="""""")
class TagDeleteGQLModel:
    name: str
    id: Optional[strawberry.ID] = None

@strawberry.type
class TagResultGQLModel:
    id: Union[strawberry.ID, None] = None
    msg: str = None

    @strawberry.field(description="""Result of drone operation""")
    async def tag(self, info: strawberry.types.Info) -> Union[PreferenceTagGQLModel, None]:
        result = await PreferenceTagGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation
async def tag_insert(self, info: strawberry.types.Info, tag: TagInsertGQLModel) -> TagResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).tags
    tag.changedby = actingUser["id"]
    tag.author_id = actingUser["id"]
    result = TagResultGQLModel()
    rows = await loader.filter_by(name=tag.name)
    row = next(rows, None)
    if row is None:
        row = await loader.insert(tag)
        result.id = row.id
        result.msg = "ok"
    else:
        result.id = row.id
        result.msg = "fail"
    return result

@strawberry.mutation("""""")
async def tag_delete(self, info: strawberry.types.Info, tag: TagDeleteGQLModel) -> TagResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).tags
    
    result = TagResultGQLModel()
    result.id = tag.id
    if tag.id is None:
        rows = await loader.filter_by(author_id=actingUser["id"])
        rows = await loader.filter_by(name=tag.name, author_id=actingUser["id"])
        row = next(rows, None)
    else:
        row = await loader.load(tag.id)

    if row is None:
        result.msg = "fail"
    else:
        await loader.delete(row.id)
        result.msg = "ok"
        result.id = None
        
    return result

@strawberry.mutation("""""")
async def tag_update(self, info: strawberry.types.Info, tag: TagUpdateGQLModel) -> TagResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).tags
    tag.updatedby = actingUser["id"]

    result = TagResultGQLModel()
    result.id = tag.id
    row = await loader.update(tag)
    if row is None:
        result.msg = "fail"
    else:
        result.msg = "ok"        
    return result

# import datetime

# @strawberry.input(description="""""")
# class DroneInsertGQLModel:
#     name: str
#     id: Optional[strawberry.ID] = None
#     createdby: strawberry.Private[strawberry.ID] = None
#     longitude: Optional[float] = None
#     latitude: Optional[float] = None
#     z: Optional[float] = None

# @strawberry.input(description="""""")
# class DroneUpdateGQLModel:
#     id: strawberry.ID
#     name: Optional[str] = None
#     lastchange: datetime.datetime
#     changedby: strawberry.Private[strawberry.ID] = None
#     longitude: Optional[float] = None
#     latitude: Optional[float] = None
#     z: Optional[float] = None
#     scenario_id: Optional[Union[strawberry.ID, None]] = None
    
# @strawberry.type
# class DroneResultGQLModel:
#     id: strawberry.ID = None
#     msg: str = None

#     @strawberry.field(description="""Result of drone operation""")
#     async def drone(self, info: strawberry.types.Info) -> Union[DroneGQLModel, None]:
#         result = await DroneGQLModel.resolve_reference(info, self.id)
#         return result

# @strawberry.mutation
# async def drone_insert(self, info: strawberry.types.Info, drone: DroneInsertGQLModel) -> DroneResultGQLModel:
#     actingUser = getUser(info)
#     loader = getLoaders(info).drones
#     drone.createdby = actingUser["id"]
#     row = await loader.insert(drone)
#     result = DroneResultGQLModel()
#     result.msg = "ok"
#     result.id = row.id
#     return result

# @strawberry.mutation
# async def drone_update(self, info: strawberry.types.Info, drone: DroneUpdateGQLModel) -> DroneResultGQLModel:
#     actingUser = getUser(info)
#     loader = getLoaders(info).drones
#     drone.changedby = actingUser["id"]
#     row = await loader.update(drone)
#     result = DroneResultGQLModel()
#     result.id = drone.id
#     if row is None:
#         result.msg = "fail"
#     else:
#         result.msg = "ok"
#     return result


# from api.resolvers import DroneRemoveFromScenario

# @strawberry.mutation
# async def drone_remove_from_scenario(self, info: strawberry.types.Info, drone_id: strawberry.ID) -> DroneResultGQLModel:
#     asyncSessionMaker = info.context["asyncSessionMaker"]

#     await DroneRemoveFromScenario(asyncSessionMaker, drone_id=drone_id)
    
#     # actingUser = getUser(info)
#     # loader = getLoaders(info).drones
#     # drone = await loader.load(drone_id)
#     # drone.changedby = actingUser["id"]
#     # drone.scenario_id = None
#     # row = await loader.update(drone)
#     # print(row.scenario_id)
#     result = DroneResultGQLModel()
#     # result.id = drone.id
#     result.id = drone_id
#     result.msg = "ok"
#     # if row is None:
#     #     result.msg = "fail"
#     # else:
#     #     result.msg = "ok"
#     return result

# #####################################################################
# #
# # Special resolvers
# #
# #####################################################################

# # async def drone_by_root_drone_id(root, info: strawberry.types.Info) -> Union["DroneGQLModel", None]:
# #     return await DroneGQLModel.resolve_reference(info=info, id=root.drone_id)

