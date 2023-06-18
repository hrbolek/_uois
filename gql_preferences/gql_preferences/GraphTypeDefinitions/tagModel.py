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

    @strawberry.field(description="""entities marked with this tag""")
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

@strawberry.input(description="""Creates a new tag""")
class TagInsertGQLModel:
    name: str = strawberry.field(default="new tag", description="tag name")
    id: Optional[strawberry.ID] = strawberry.field(default=None, description="optional primary key value of tag, UUID expected")
    createdby: strawberry.Private[strawberry.ID] = None #strawberry.field(default=None, description="user who created this db record")
    author_id: strawberry.Private[strawberry.ID] = None #strawberry.field(default=None, description="user who owns this tag")

@strawberry.input(description="""Updates the tag""")
class TagUpdateGQLModel:
    id: strawberry.ID = strawberry.field(default=None, description="primary key value, aka tag identification")
    name: str = strawberry.field(default=None, description="tag name")
    lastchange: datetime.datetime = strawberry.field(default=None, description="timestamp")
    updatedby: strawberry.Private[strawberry.ID] = None #strawberry.field(default=None, description="user who updates the tag")

@strawberry.input(description="""Removes the tag""")
class TagDeleteGQLModel:
    name: str = strawberry.field(default=None, description="tag name, could be used as an identification")
    id: Optional[strawberry.ID] = strawberry.field(default=None, description="primary key, aka tag identification")

@strawberry.type(description="""result of tag operation""")
class TagResultGQLModel:
    id: Union[strawberry.ID, None] = strawberry.field(default=None, description="id of tag")
    msg: str = strawberry.field(default=None, description="""result of operation, should be "ok" or "fail" """)

    @strawberry.field(description="""Result of drone operation""")
    async def tag(self, info: strawberry.types.Info) -> Union[PreferenceTagGQLModel, None]:
        result = await PreferenceTagGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(description="inserts a new tag, if the name is already defined, operation will fail")
async def tag_insert(self, info: strawberry.types.Info, tag: TagInsertGQLModel) -> TagResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).tags
    tag.changedby = actingUser["id"]
    tag.author_id = actingUser["id"]
    result = TagResultGQLModel()
    rows = await loader.filter_by(name=tag.name, author_id=actingUser["id"])
    row = next(rows, None)
    if row is None:
        row = await loader.insert(tag)
        result.id = row.id
        result.msg = "ok"
    else:
        result.id = row.id
        result.msg = "fail"
    return result

@strawberry.mutation(description="""deletes the tag""")
async def tag_delete(self, info: strawberry.types.Info, tag: TagDeleteGQLModel) -> TagResultGQLModel:
    actingUser = getUser(info)
    loader = getLoaders(info).tags
    
    result = TagResultGQLModel()
    result.id = tag.id
    if tag.id is None:
        # rows = await loader.filter_by(author_id=actingUser["id"])
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

@strawberry.mutation(description="""updates the tag""")
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
