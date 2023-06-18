import strawberry
import datetime
from typing import Union, Optional, List, TYPE_CHECKING, Annotated

from .externals import UserGQLModel, GroupGQLModel, FacilityGQLModel, EventGQLModel

def getLoaders(info):
    return info.context["all"]

def getUser(info):
    return info.context["user"]

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a tag / label which can be assigned to entities""",
)
class PreferenceTagEntityGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        if id is None:
            return None
        loader = getLoaders(info).tagentities
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
    async def value(self, info: strawberry.types.Info) -> Union[str, None]:
        return self.value

    @strawberry.field(description="""Entities associated with this tag""")
    async def entities(self, info: strawberry.types.Info) -> List[Union[UserGQLModel, GroupGQLModel]]:
        loader = getLoaders(info).tagentities
        rows = await loader.filter_by(tag_id=self.tag_id)
        result = []
        for row in rows:
            entity_type_id = row.entity_type_id
            entity_id = row.entity_id
            entityClass = entity_type_ids.get(entity_type_id, None)
            if entityClass is not None:
                entity = await entityClass.resolve_reference(id=entity_id)
                result.append(entity)
        return result


#####################################################################
#
# Special fields for query
#
#####################################################################
@strawberry.type(description="""represents a GQL model""")
class PreferenceEntityIdGQLModel:

    @strawberry.field(description="""primary key""")
    async def model_id(self, info: strawberry.types.Info) -> strawberry.ID:
        return self["id"]

    @strawberry.field(description="""GQL model name""")
    async def model_name(self, info: strawberry.types.Info) -> str:
        return self["name"]

entity_type_ids = {
    "e8479a21-b7c4-4140-9562-217de2656d55": UserGQLModel,
    "2d3d9801-0017-4cf2-9272-2df7b59da667": GroupGQLModel,
    "a7457888-ed8a-4720-b116-13558cd7963b": EventGQLModel,
    "9feb8037-6c62-45bb-ac20-916763731f5d": FacilityGQLModel
}

import logging

tags_description = """Returns list of hardwired models for tags."""
@strawberry.field(description=tags_description)
async def preference_entity_tags(info: strawberry.types.Info) -> List["PreferenceEntityIdGQLModel"]:
    result = list(map(lambda item: {"id": item[0], "name": item[1]._type_definition.name}, entity_type_ids.items()))
    return result

tags_description = """Returns list of tags for the entity."""
@strawberry.field(description=tags_description)
async def preference_tags_for_entity(info: strawberry.types.Info, entity_id: strawberry.ID) -> List["PreferenceTagEntityGQLModel"]:
    actingUser = getUser(info)
    actingUserId = actingUser["id"]
    loader = getLoaders(info).tagentities
    result = await loader.filter_by(author_id=actingUserId, entity_id=entity_id)
    return result

entities_description = """Returns list of entities labeled by tags."""
@strawberry.field(description=entities_description)
async def preference_entities(info: strawberry.types.Info, tags: List[strawberry.ID]) -> List["PreferenceTagEntityGQLModel"]:
    # TODO
    idsSet = set(tags)
    actingUser = getUser(info)
    actingUserId = actingUser["id"]

    loader = getLoaders(info).tagentities
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        stmt = loader.getSelectStatement()
        model = loader.getModel()
        
        fullstmt = stmt.filter_by(author_id=actingUserId).filter(model.tag_id.in_(tags))#.group_by("entity_id")
        #rows = await session.execute(fullstmt)
        rows = await loader.execute_select(fullstmt)
        indexed = {}
        for row in rows:
            key = row.entity_id
            indexedvalue = indexed.get(key, None)
            if indexedvalue is None:
                indexedvalue = {"tags": set(), "type": row.entity_type_id}
                indexed[key] = indexedvalue
            indexedvalue["tags"].add(row.tag_id)
        results = filter(lambda item: idsSet.issubset(item[1]["tags"]), indexed.items())
        resultList = []
        for id, value in results:
            cls = entity_type_ids[value["type"]]
            resultList.append(await cls.resolve_reference(id=id))
        #print(resultList)
        return resultList

#####################################################################
#
# Mutation section
#
#####################################################################

# import datetime

@strawberry.input(description="""allows to create link between an GQL entity, tag and user who defined it""")
class EntityAddTagGQLModel:
    entity_id: strawberry.ID = strawberry.field(default=None, description="GQL entity primary key value, aka GQL entity identification")
    entity_type_id: strawberry.ID = strawberry.field(default=None, description="GQL entity type, aka UserGQLModel id")
    tag_id: strawberry.ID = strawberry.field(default=None, description="tag identification")
    createdby: strawberry.Private[strawberry.ID] = None #strawberry.field(default=None, description="User who created and assigned the tag")

@strawberry.input(description="""removes a tag from entity""")
class EntityRemoveTagGQLModel:
    entity_id: strawberry.ID = strawberry.field(default=None, description="GQL entity primary key value, aka GQL entity identification")
    tag_id: strawberry.ID = strawberry.field(default=None, description="tag identification")
    id: Optional[strawberry.ID] = strawberry.field(default=None, description="direct identification of the link, if not given, other two ids are used together")

@strawberry.type(description="reports the result of operation")
class EntityTagResultGQLModel:
    msg: str = strawberry.field(default=None, description="""result of operation, should be "ok" or "fail" """)
    id: Optional[strawberry.ID] = strawberry.field(default=None, description="tag id, could be undefined if the operation was delete")
    @strawberry.field(description="""""")
    async def tag(self, info: strawberry.types.Info) -> Union[PreferenceTagEntityGQLModel, None]:
        result = await PreferenceTagEntityGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(description="""Marks an entity with a tag""")
async def tag_add_to_entity(self, info: strawberry.types.Info, tag_data: EntityAddTagGQLModel) -> EntityTagResultGQLModel:
    assert tag_data.entity_type_id in entity_type_ids, "unknown entity type"
    actingUser = getUser(info)
    loader = getLoaders(info).tagentities
    rows = await loader.filter_by(tag_id=tag_data.tag_id, entity_id=tag_data.entity_id)
    row = next(rows, None)
    result = EntityTagResultGQLModel()
    if row is None:
        row = await loader.insert(tag_data)
        result.id = row.id
        result.msg = "ok"
    else:
        result.id = row.id
        result.msg = "fail"
    return result

@strawberry.mutation(description="""Removes a tag from entity""")
async def tag_remove_from_entity(self, info: strawberry.types.Info, tag_data: EntityRemoveTagGQLModel) -> EntityTagResultGQLModel:
    
    actingUser = getUser(info)
    loader = getLoaders(info).tagentities
    if tag_data.id is None:
        rows = await loader.filter_by(tag_id=tag_data.tag_id, entity_id=tag_data.entity_id)
        row = next(rows, None)
    else:
        row = await loader.load(tag_data.id)

    result = EntityTagResultGQLModel()
    if row is None:
        result.id = tag_data.id
        result.msg = "fail"
    else:
        await loader.delete(row.id)
        result.id = None
        result.msg = "ok"
    return result



#####################################################################
#
# Special resolvers
#
#####################################################################



