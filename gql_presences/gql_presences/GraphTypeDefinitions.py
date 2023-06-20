from typing import List, Union
import typing
from unittest import result
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


def AsyncSessionFromInfo(info):
    print(
        "obsolete function used AsyncSessionFromInfo, use withInfo context manager instead"
    )
    return info.context["session"]

def getLoaders(info):
    return info.context['all']
###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
#
# priklad rozsireni UserGQLModel
#

from gql_presences.GraphResolvers import (
    resolveTaskModelByPage,
    resolveTaskModelById,
    resolveTasksForUser,
)
from gql_presences.GraphResolvers import (
    resolveContentModelByPage,
    resolveContentModelById,
    resolveContentForEvent,
)



@strawberryA.federation.type(keys=["id"], description="""Entity representing tasks""")
class TaskGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveTaskModelById(session, id)
            result._type_definition = cls._type_definition
            return result

    @strawberryA.field(description="""Primary key of task""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Name of tasks""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Brief description""")
    def brief_des(self) -> Union[str, None]:
        return self.brief_des

    @strawberryA.field(description="""Full description""")
    def detailed_des(self) -> Union[str, None]:
        return self.detailed_des

    @strawberryA.field(description=""" Reference""")
    def reference(self) -> Union[str, None]:
        return self.reference

    @strawberryA.field(description="""Date of entry""")
    def date_of_entry(self) -> datetime.date:
        return self.date_of_entry

    @strawberryA.field(description="""Date of submission""")
    def date_of_submission(self) -> Union[datetime.date, None]:
        return self.date_of_submission

    @strawberryA.field(description="""Date of fullfilment""")
    def date_of_fulfillment(self) -> Union[datetime.date, None]:
        return self.date_of_fulfillment

    @strawberryA.field(description="""event id""")
    async def event(self, info: strawberryA.types.Info) -> Union["EventGQLModel", None]:
        if self.event_id is None:
            result = None
        else:
            result = await EventGQLModel(id=self.event_id)
        return result

    @strawberryA.field(description="""event id""")
    async def user(self, info: strawberryA.types.Info) -> Union["UserGQLModel", None]:
        if self.user_id is None:
            result = None
        else:
            result = await UserGQLModel(id=self.user_id)
        return result


@strawberryA.federation.type(keys=["id"], description="""Entity representing content""")
class ContentGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveContentModelById(session, id)
            result._type_definition = cls._type_definition
            return result

    @strawberryA.field(description="""Primary key of content""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Brief description""")
    def brief_desc(self) -> str:
        return self.brief_des

    @strawberryA.field(description="""Full description""")
    def detailed_desc(self) -> str:
        return self.detailed_des

    @strawberryA.field(description="""event id""")
    async def event(self, info: strawberryA.types.Info) -> Union["EventGQLModel", None]:
        if self.event_id is None:
            result = None
        else:
            result = EventGQLModel(id=self.event_id)
        return result

    # DODĚLAT BRIEF A FULL DESC


@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz

    @strawberryA.field(description="""task id""")
    async def tasks(self, info: strawberryA.types.Info) -> typing.List["TaskGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveTasksForUser(session, self.id)
            return result


@strawberryA.federation.type(extend=True, keys=["id"])
class EventGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return EventGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz

    # rozšiřujeme jen o atributy (1,1)
    @strawberryA.field(description="""content id""")
    async def content(
        self, info: strawberryA.types.Info
    ) -> typing.Union["ContentGQLModel", None]:
        async with withInfo(info) as session:
            result = await resolveContentForEvent(
                session, self.id
            )  # z tabulky obsahů hledáme event_id = event_id v Content
            return next(result, None)

    @strawberryA.field(description="""tasks assiciated with this event""")
    async def tasks(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> List[TaskGQLModel]:
        loader = getLoaders(info).tasks
        result = await loader.filter_by(event_id=self.id)
        return result

#     zde je rozsireni o dalsi resolvery¨
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(session,  self.id)
#         return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
from gql_presences.GraphResolvers import resolveTasksForEvent


@strawberryA.type(description="""Type for query root""")
class Query:
    # nedotazovat se na TaskOnEventModel
    @strawberryA.field(description="""Finds a workflow by their id""")
    async def say_hello_presences(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result

    @strawberryA.field(description="""Finds tasks by their id""")
    async def task_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[TaskGQLModel, None]:
        result = await TaskGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds tasks by their page""")
    async def task_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[TaskGQLModel]:
        loader = getLoaders(info).tasks
        result = await loader.page(skip=skip, limit=limit)
        return result

    @strawberryA.field(description="""Finds presence by their id""")
    async def tasks_by_event(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> List[TaskGQLModel]:
        loader = getLoaders(info).tasks
        result = await loader.filter_by(event_id=id)
        return result

    @strawberryA.field(description="""Finds content by their id""")
    async def content_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[ContentGQLModel, None]:
        result = await ContentGQLModel.resolve_reference(info, id)
        return result

    @strawberryA.field(description="""Finds content by their page""")
    async def content_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[ContentGQLModel]:
        loader = getLoaders(info).contents
        result = await loader.page(skip=skip, limit=limit)
        return result

    # 264 - 267
    # volat funkci
    #

    # radnomPresenceData
    # async def ....
    # zavolat funkci
    # předat výstup výsledku dotazu
    # vrátit hlavní datovou strukturu
    # resolvePresenceModelById


###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

from typing import Optional

@strawberryA.input
class TaskInsertGQLModel:
    name: str
    user_id: strawberryA.ID

    brief_des: Optional[str] = ""
    detailed_des: Optional[str] = "" 
    reference: Optional[str] = ""
    date_of_entry: Optional[datetime.datetime] = datetime.datetime.now()
    date_of_submission: Optional[datetime.datetime] = datetime.datetime.now()
    date_of_fulfillment: Optional[datetime.datetime] = datetime.datetime.now() + datetime.timedelta(days=7)

    event_id: Optional[strawberryA.ID] = None
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class TaskUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str]

    brief_des: Optional[str] = None
    detailed_des: Optional[str] = None
    reference: Optional[str] = None
    date_of_entry: Optional[datetime.datetime] = None
    date_of_submission: Optional[datetime.datetime] = None
    date_of_fulfillment: Optional[datetime.datetime] = None
    event_id: Optional[strawberryA.ID] = None
    
@strawberryA.type
class TaskResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def task(self, info: strawberryA.types.Info) -> Union[TaskGQLModel, None]:
        result = await TaskGQLModel.resolve_reference(info, self.id)
        return result
   
@strawberryA.type
class Mutation:
    @strawberryA.mutation(description="Adds a task.")
    async def task_insert(self, info: strawberryA.types.Info, task: TaskInsertGQLModel) -> TaskResultGQLModel:
        loader = getLoaders(info).tasks
        row = await loader.insert(task)
        result = TaskResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="Update the task.")
    async def task_update(self, info: strawberryA.types.Info, task: TaskUpdateGQLModel) -> TaskResultGQLModel:
        loader = getLoaders(info).tasks
        row = await loader.update(task)
        result = TaskResultGQLModel()
        result.msg = "ok"
        result.id = task.id
        if row is None:
            result.msg = "fail"
            
        return result
    
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, EventGQLModel), mutation=Mutation)
