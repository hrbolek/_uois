from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager
import datetime

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
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)  # jestlize rozsirujete, musi byt tento vyraz


#     zde je rozsireni o dalsi resolvery
#     @strawberryA.field(description="""Inner id""")
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(session,  self.id)
#         return result


@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)


@strawberryA.federation.type(extend=True, keys=["id"])
class FacilityGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return FacilityGQLModel(id=id)


@strawberryA.federation.type(extend=True, keys=["id"])
class EventGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return EventGQLModel(id=id)


@strawberryA.federation.type(extend=True, keys=["id"])
class AcTopicGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return AcTopicGQLModel(id=id)


@strawberryA.federation.type(extend=True, keys=["id"])
class AcSemesterGQLModel:

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return AcSemesterGQLModel(id=id)


from gql_lessons.GraphResolvers import (
    resolvePlannedLessonById,
    resolvePlannedLessonPage,
    resolveUserLinksForPlannedLesson,
    resolveGroupLinksForPlannedLesson,
    resolveFacilityLinksForPlannedLesson,
    # resolveEventLinksForPlannedLesson,
    resolvePlannedLessonsByLink,
)


@strawberryA.federation.type(
    keys=["id"],
    description="""Entity representing a planned lesson for timetable creation""",
)
class PlannedLessonGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolvePlannedLessonById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Timestap""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""primary key""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""primary key""")
    def length(self) -> int:
        return self.length

    @strawberryA.field(
        description="""planned lesson linked to (aka master planned lesson)"""
    )
    async def linked_to(
        self, info: strawberryA.types.Info
    ) -> Union["PlannedLessonGQLModel", None]:
        async with withInfo(info) as session:
            if self.linkedlesson_id is None:
                result = None
            else:
                result = await resolvePlannedLessonById(session, self.linkedlesson_id)
            return result

    @strawberryA.field(
        description="""planned lessons linked with, even trought master, including self"""
    )
    async def linked_with(
        self, info: strawberryA.types.Info
    ) -> List["PlannedLessonGQLModel"]:
        async with withInfo(info) as session:
            if self.linkedlesson_id is None:
                # I am the master, but possibly without followers
                result = await resolvePlannedLessonsByLink(session, self.id)
                result = list(result)
                result2 = [self, *result]
            else:
                # I am the follower
                master = await resolvePlannedLessonById(session, self.linkedlesson_id)
                result = await resolvePlannedLessonsByLink(
                    session, self.linkedlesson_id
                )
                result = list(result)
                result2 = [master, *result]
            return result2

    @strawberryA.field(description="""teachers""")
    async def users(self, info: strawberryA.types.Info) -> List["UserGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveUserLinksForPlannedLesson(session, self.id)
            result2 = [UserGQLModel(id=item.user_id) for item in result]
            return result2

    @strawberryA.field(description="""study groups""")
    async def groups(self, info: strawberryA.types.Info) -> List["GroupGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveGroupLinksForPlannedLesson(session, self.id)
            result2 = [GroupGQLModel(id=item.user_id) for item in result]
            return result2

    @strawberryA.field(description="""facilities""")
    async def facilities(
        self, info: strawberryA.types.Info
    ) -> List["FacilityGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveFacilityLinksForPlannedLesson(session, self.id)
            result2 = [FacilityGQLModel(id=item.user_id) for item in result]
            return result2

    @strawberryA.field(description="""linked event""")
    async def event(self, info: strawberryA.types.Info) -> Union["EventGQLModel", None]:
        async with withInfo(info) as session:
            # result = await resolveEventLinksForPlannedLesson(session, self.id)
            # result2 = [EventGQLModel(id=item.user_id) for item in result]
            # return result2
            if self.event_id is None:
                result = None
            else:
                result = EventGQLModel(id=self.event_id)
            return result

    @strawberryA.field(description="""linked topic from accreditation""")
    async def topic(
        self, info: strawberryA.types.Info
    ) -> Union["AcTopicGQLModel", None]:
        async with withInfo(info) as session:
            if self.topic_id is None:
                result = None
            else:
                result = AcTopicGQLModel(id=self.topic_id)
            return result

    @strawberryA.field(
        description="""linked subject semester from program (accreditation)"""
    )
    async def semester(
        self, info: strawberryA.types.Info
    ) -> Union["AcSemesterGQLModel", None]:
        async with withInfo(info) as session:
            if self.semester_id is None:
                result = None
            else:
                result = AcSemesterGQLModel(id=self.semester_id)
            return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
from gql_lessons.GraphResolvers import (
    resolvePlannedLessonBySemester,
    resolvePlannedLessonByTopic,
    resolvePlannedLessonByEvent,
)


@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""just a check""")
    async def say_hello(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result

    @strawberryA.field(description="""Planned lesson by its id""")
    async def planned_lesson_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[PlannedLessonGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonById(session, id)
            return result

    @strawberryA.field(description="""Planned lesson paged""")
    async def planned_lesson_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[PlannedLessonGQLModel]:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonPage(session, skip, limit)
            return result

    @strawberryA.field(description="""Planned lesson by its semester (subject)""")
    async def planned_lessons_by_semester(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> List[PlannedLessonGQLModel]:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonBySemester(session, id)
            return result

    @strawberryA.field(description="""Planned lesson by its topic""")
    async def planned_lessons_by_topic(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> List[PlannedLessonGQLModel]:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonByTopic(session, id)
            return result

    @strawberryA.field(description="""Planned lesson """)
    async def planned_lessons_by_event(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> List[PlannedLessonGQLModel]:
        async with withInfo(info) as session:
            result = await resolvePlannedLessonByEvent(session, id)
            return result


###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

from typing import Optional

@strawberryA.input
class PlannedLessonInsertGQLModel:
    name: str

    length: Optional[int] = 2
    startproposal: Optional[datetime.datetime] = None

    linkedlesson_id: Optional[strawberryA.ID] = None
    topic_id: Optional[strawberryA.ID] = None
    lessontype_id: Optional[strawberryA.ID] = None
    semester_id: Optional[strawberryA.ID] = None
    event_id: Optional[strawberryA.ID] = None
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class PlannedLessonUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str] = None
    length: Optional[int] = None
    startproposal: Optional[datetime.datetime] = None

    linkedlesson_id: Optional[strawberryA.ID] = None
    topic_id: Optional[strawberryA.ID] = None
    lessontype_id: Optional[strawberryA.ID] = None
    semester_id: Optional[strawberryA.ID] = None
    event_id: Optional[strawberryA.ID] = None
    
@strawberryA.type
class PlannedLessonResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def lesson(self, info: strawberryA.types.Info) -> Union[PlannedLessonGQLModel, None]:
        result = await PlannedLessonGQLModel.resolve_reference(info, self.id)
        return result


    
@strawberryA.federation.type(extend=True)
class Mutation:
    @strawberryA.mutation
    async def planned_lesson_insert(self, info: strawberryA.types.Info, lesson: PlannedLessonInsertGQLModel) -> PlannedLessonResultGQLModel:
        loader = getLoaders(info).plans
        row = await loader.insert(lesson)
        result = PlannedLessonResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation
    async def planned_lesson_update(self, info: strawberryA.types.Info, lesson: PlannedLessonUpdateGQLModel) -> PlannedLessonResultGQLModel:
        loader = getLoaders(info).plans
        row = await loader.update(lesson)
        result = PlannedLessonResultGQLModel()
        result.msg = "ok"
        result.id = lesson.id
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

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel,), mutation=Mutation)
