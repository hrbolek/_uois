from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
from contextlib import asynccontextmanager

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context['asyncSessionMaker']
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass



def AsyncSessionFromInfo(info):
    print('obsolete function used AsyncSessionFromInfo, use withInfo context manager instead')
    return info.context['session']

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
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id) # jestlize rozsirujete, musi byt tento vyraz

#     zde je rozsireni o dalsi resolvery
#     @strawberryA.field(description="""Inner id""")
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(session,  self.id)
#         return result

@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)

@strawberryA.federation.type(extend=True, keys=["id"])
class FacilityGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return FacilityGQLModel(id=id) 
@strawberryA.federation.type(extend=True, keys=["id"])
class EventGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return EventGQLModel(id=id) 




from gql_lessons.GraphResolvers import resolvePlannedLessonById, resolvePlannedLessonPage ,resolveUserLinksForPlannedLesson, resolveGroupLinksForPlannedLesson, resolveFacilityLinksForPlannedLesson,resolveEventLinksForPlannedLesson
                                     
                                    

@strawberryA.federation.type(keys=["id"], description="""Entity representing a planned lesson for timetable creation""")
class PlannedLessonGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolvePlannedLessonById(session,  id)
        result._type_definition = cls._type_definition # little hack :)
        return result 
          
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""primary key""")
    async def users(self, info: strawberryA.types.Info) -> List["UserGQLModel"]:
        result = await resolveUserLinksForPlannedLesson(session, self.id)
        result2 = [UserGQLModel(id=item.user_id) for item in result]
        return result2

    @strawberryA.field(description="""primary key""")
    async def groups(self, info: strawberryA.types.Info) -> List["GroupGQLModel"]: 
        result = await resolveGroupLinksForPlannedLesson(session, self.id)
        result2 = [GroupGQLModel(id=item.user_id) for item in result]
        return result2

    @strawberryA.field(description="""primary key""")
    async def facilities(self, info: strawberryA.types.Info) -> List["FacilityGQLModel"]: 
        result = await resolveFacilityLinksForPlannedLesson(session, self.id)
        result2 = [FacilityGQLModel(id=item.user_id) for item in result]
        return result2

    @strawberryA.field(description="""primary key""")
    async def events(self, info: strawberryA.types.Info) -> List["EventGQLModel"]: 
        result = await resolveEventLinksForPlannedLesson(session, self.id)
        result2 = [EventGQLModel(id=item.user_id) for item in result]
        return result2

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result


    async def planned_lesson_by_id(self,info: strawberryA.types.Info, id: uuid.UUID) -> Union[PlannedLessonGQLModel,None]:
        result = await resolvePlannedLessonById(session,  id)
        return result

    async def planned_lesson_page(self,info: strawberryA.types.Info,skip: int = 0, limit: int = 10) -> List[PlannedLessonGQLModel]:
        result = await resolvePlannedLessonPage(session,  skip, limit)
        return result

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))