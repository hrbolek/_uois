from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid
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
# GQL PROJECT
import datetime
from gql_projects.GraphResolvers import (
    resolveProjectById,
    resolveProjectAll,
    resolveUpdateProject,
    resolveInsertProject,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a project"""
)
class ProjectGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).projects
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Start date""")
    def startdate(self) -> datetime.date:
        return self.startdate

    @strawberryA.field(description="""End date""")
    def enddate(self) -> datetime.date:
        return self.enddate

    @strawberryA.field(description="""Last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Last change""")
    async def team(self) -> Union["GroupGQLModel", None]:
        result = await GroupGQLModel.resolve_reference(self.group_id)
        return result

    @strawberryA.field(description="""Project type of project""")
    async def project_type(self, info: strawberryA.types.Info) -> "ProjectTypeGQLModel":
        result = await ProjectTypeGQLModel.resolve_reference(info, self.projecttype_id)
        return result

    @strawberryA.field(description="""List of finances, related to a project""")
    async def finances(
        self, info: strawberryA.types.Info
    ) -> typing.List["FinanceGQLModel"]:
        loader = getLoaders(info).finances
        result = await loader.filter_by(project_id=self.id)
        return result

    @strawberryA.field(description="""List of milestones, related to a project""")
    async def milestones(
        self, info: strawberryA.types.Info
    ) -> typing.List["MilestoneGQLModel"]:
        loader = getLoaders(info).milestones
        result = await loader.filter_by(project_id=self.id)
        return result

    @strawberryA.field(description="""Group, related to a project""")
    async def group(self, info: strawberryA.types.Info) -> "GroupGQLModel":
        return GroupGQLModel(id=self.group_id)


# GQL PROJECT TYPE
from gql_projects.GraphResolvers import (
    resolveProjectTypeById,
    resolveProjectTypeAll,
    resolveUpdateProjectType,
    resolveInsertProjectType,
    resolveProjectsForProjectType,
    resolveFinancesForProject,
    resolveMilestonesForProject,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a project types"""
)
class ProjectTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).projecttypes
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""List of projects, related to project type""")
    async def projects(
        self, info: strawberryA.types.Info
    ) -> typing.List["ProjectGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveProjectsForProjectType(session, self.id)
            return result


# GQL FINANCE
from gql_projects.GraphResolvers import (
    resolveFinanceById,
    resolveFinanceAll,
    resolveUpdateFinance,
    resolveInsertFinance,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a finance"""
)
class FinanceGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).finances
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Time stamp""")
    def lastchange(self) -> strawberryA.ID:
        return self.lastchange

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Amount""")
    def amount(self) -> float:
        return self.amount

    @strawberryA.field(description="""Last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Project of finance""")
    async def project(self, info: strawberryA.types.Info) -> "ProjectGQLModel":
        async with withInfo(info) as session:
            result = await resolveProjectById(session, self.project_id)
            return result

    @strawberryA.field(description="""Finance type of finance""")
    async def financeType(self, info: strawberryA.types.Info) -> "FinanceTypeGQLModel":
        async with withInfo(info) as session:
            result = await resolveFinanceTypeById(session, self.financetype_id)
            return result


# GQL FINANCE TYPE
from gql_projects.GraphResolvers import (
    resolveFinanceTypeById,
    resolveFinanceTypeAll,
    resolveUpdateFinanceType,
    resolveInsertFinanceType,
    resolveFinancesForFinanceType,
)


@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a finance type"""
)
class FinanceTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).financetypes
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Name""")
    def name_en(self) -> str:
        return self.name_en

    @strawberryA.field(description="""List of finances, related to finance type""")
    async def finances(
        self, info: strawberryA.types.Info
    ) -> typing.List["FinanceGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveFinancesForFinanceType(session, self.id)
            return result


# GQL MILESTONE
from gql_projects.GraphResolvers import (
    resolveMilestoneById,
    resolveMilestoneAll,
    resolveUpdateMilestone,
    resolveInsertMilestone,
)

import asyncio

@strawberryA.federation.type(
    keys=["id"], description="""Entity representing a milestone"""
)
class MilestoneGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        loader = getLoaders(info).milestones
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Time stamp""")
    def lastchange(self) -> strawberryA.ID:
        return self.lastchange

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Date""")
    def startdate(self) -> datetime.date:
        return self.startdate

    @strawberryA.field(description="""Date""")
    def enddate(self) -> datetime.date:
        return self.enddate

    @strawberryA.field(description="""Last change""")
    def lastChange(self) -> datetime.datetime:
        return self.lastChange

    @strawberryA.field(description="""Project of milestone""")
    async def project(self, info: strawberryA.types.Info) -> "ProjectGQLModel":
        async with withInfo(info) as session:
            result = await resolveProjectById(session, self.project_id)
            return result

    @strawberryA.field(description="""Milestones which has this one as follower""")
    async def previous(self, info: strawberryA.types.Info) -> List["MilestoneGQLModel"]:
        # async with withInfo(info) as session:
        #     result = await resolveProjectById(session, self.project_id)
        #     return result
        loader = getLoaders(info).milestonelinks
        rows = await loader.filter_by(next_id=self.id)
        awaitable = (MilestoneGQLModel.resolve_reference(info, row.previous_id) for row in rows)
        return await asyncio.gather(*awaitable)

    @strawberryA.field(description="""Milestone which follow this milestone""")
    async def nexts(self, info: strawberryA.types.Info) -> List["MilestoneGQLModel"]:
        # async with withInfo(info) as session:
        #     result = await resolveProjectById(session, self.project_id)
        #     return result
        loader = getLoaders(info).milestonelinks
        rows = await loader.filter_by(previous_id=self.id)
        awaitable = (MilestoneGQLModel.resolve_reference(info, row.next_id) for row in rows)
        return await asyncio.gather(*awaitable)


# GQL GROUP
from gql_projects.GraphResolvers import resolveProjectsForGroup


@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)

    @strawberryA.field(description="""List of projects, related to group""")
    async def projects(
        self, info: strawberryA.types.Info
    ) -> typing.List["ProjectGQLModel"]:
        async with withInfo(info) as session:
            result = await resolveProjectsForGroup(session, self.id)
            return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

from gql_projects.DBFeeder import randomDataStructure


@strawberryA.type(description="""Type for query root""")
class Query:
    @strawberryA.field(description="""Returns a list of projects""")
    async def project_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[ProjectGQLModel]:
        async with withInfo(info) as session:
            result = await resolveProjectAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns project by its id""")
    async def project_by_id(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> Union[ProjectGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveProjectById(session, id)
            return result

    @strawberryA.field(description="""Returns a list of project types""")
    async def project_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[ProjectTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveProjectTypeAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns a list of finances""")
    async def finance_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[FinanceGQLModel]:
        async with withInfo(info) as session:
            result = await resolveFinanceAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns a list of finance types""")
    async def finance_type_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[FinanceTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveFinanceTypeAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns a list of milestones""")
    async def milestone_page(
        self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10
    ) -> List[MilestoneGQLModel]:
        async with withInfo(info) as session:
            result = await resolveMilestoneAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns a list of projects for group""")
    async def project_by_group(
        self, info: strawberryA.types.Info, id: strawberryA.ID
    ) -> List[ProjectGQLModel]:
        async with withInfo(info) as session:
            result = await resolveProjectsForGroup(session, id)
            return result

    @strawberryA.field(description="""Random publications""")
    async def randomProject(
        self, info: strawberryA.types.Info
    ) -> Union[ProjectGQLModel, None]:
        async with withInfo(info) as session:
            result = await randomDataStructure(AsyncSessionFromInfo(info))
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
class ProjectInsertGQLModel:
    projecttype_id: strawberryA.ID
    name: str

    id: Optional[strawberryA.ID] = None
    name: Optional[str] = "Project"
    startdate: Optional[datetime.datetime] = datetime.datetime.now()
    enddate: Optional[datetime.datetime] = datetime.datetime.now()

    group_id: Optional[strawberryA.ID] = None

@strawberryA.input
class ProjectUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID
    name: Optional[str] = None
    projecttype_id: Optional[strawberryA.ID] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    group_id: Optional[strawberryA.ID] = None
    
@strawberryA.type
class ProjectResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def project(self, info: strawberryA.types.Info) -> Union[ProjectGQLModel, None]:
        result = await ProjectGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class FinanceInsertGQLModel:
    name: str
    financetype_id: strawberryA.ID
    project_id: strawberryA.ID
    id: Optional[strawberryA.ID] = None
    amount: Optional[float] = 0

@strawberryA.input
class FinanceUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID

    name: Optional[str]
    financetype_id: Optional[strawberryA.ID]
    amount: Optional[float] = None
    
@strawberryA.type
class FinanceResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def finance(self, info: strawberryA.types.Info) -> Union[FinanceGQLModel, None]:
        result = await FinanceGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class MilestoneInsertGQLModel:
    name: str
    project_id: strawberryA.ID
    startdate: Optional[datetime.datetime] = datetime.datetime.now()
    enddate: Optional[datetime.datetime] = datetime.datetime.now() + datetime.timedelta(days=30)
    id: Optional[strawberryA.ID] = None

@strawberryA.input
class MilestoneUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberryA.ID

    name: Optional[str] = None
    startdate: Optional[datetime.datetime] = None
    enddate: Optional[datetime.datetime] = None
    
@strawberryA.type
class MilestoneResultGQLModel:
    id: strawberryA.ID = None
    msg: str = None

    @strawberryA.field(description="""Result of user operation""")
    async def milestone(self, info: strawberryA.types.Info) -> Union[MilestoneGQLModel, None]:
        result = await MilestoneGQLModel.resolve_reference(info, self.id)
        return result

@strawberryA.input
class MilestoneLinkAddGQLModel:
    previous_id: strawberryA.ID
    next_id: strawberryA.ID
    
@strawberryA.federation.type(extend=True)
class Mutation:
    @strawberryA.mutation(description="Adds a new milestones link.")
    async def milestones_link_add(self, info: strawberryA.types.Info, link: MilestoneLinkAddGQLModel) -> MilestoneResultGQLModel:
        loader = getLoaders(info).milestonelinks
        rows = await loader.filter_by(previous_id=link.previous_id, next_id=link.next_id)
        row = next(rows, None)
        result = MilestoneResultGQLModel()
        if row is None:
            row = await loader.insert(link)
            result.msg = "ok"
        else:
            result.msg = "exists"
        result.id = link.previous_id
        return result

    @strawberryA.mutation(description="Removes the milestones link.")
    async def milestones_link_remove(self, info: strawberryA.types.Info, link: MilestoneLinkAddGQLModel) -> MilestoneResultGQLModel:
        loader = getLoaders(info).milestonelinks
        rows = await loader.filter_by(previous_id=link.previous_id, next_id=link.next_id)
        row = next(rows, None)
        result = MilestoneResultGQLModel()
        if row is None:
            result.msg = "fail"
        else:
            await loader.delete(row.id)
            result.msg = "ok"
        result.id = link.previous_id
        return result

    @strawberryA.mutation(description="Adds a new milestone.")
    async def milestone_insert(self, info: strawberryA.types.Info, milestone: MilestoneInsertGQLModel) -> MilestoneResultGQLModel:
        loader = getLoaders(info).milestones
        row = await loader.insert(milestone)
        result = MilestoneResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="Update the milestone.")
    async def milestone_update(self, info: strawberryA.types.Info, milestone: MilestoneUpdateGQLModel) -> MilestoneResultGQLModel:
        loader = getLoaders(info).milestones
        row = await loader.update(milestone)
        result = MilestoneResultGQLModel()
        result.msg = "ok"
        result.id = milestone.id
        if row is None:
            result.msg = "fail"
            
        return result

    @strawberryA.mutation(description="Delete the milestone.")
    async def milestone_delete(self, info: strawberryA.types.Info, id: strawberryA.ID) -> ProjectResultGQLModel:
        loader = getLoaders(info).milestonelinks
        rows = await loader.filter_by(previous_id=id)
        linksids = [row.id for row in rows]
        rows = await loader.filter_by(next_id=id)
        linksids.extend([row.id for row in rows])
        for id in linksids:
            await loader.delete(id)

        loader = getLoaders(info).milestones
        row = await loader.load(id)
        result = ProjectResultGQLModel()
        result.id = row.project_id
        await loader.delete(id)       
        result.msg = "ok"
        return result

    @strawberryA.mutation(description="Adds a new finance record.")
    async def finance_insert(self, info: strawberryA.types.Info, finance: FinanceInsertGQLModel) -> FinanceResultGQLModel:
        loader = getLoaders(info).finances
        row = await loader.insert(finance)
        result = FinanceResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="Update the finance record.")
    async def finance_update(self, info: strawberryA.types.Info, finance: FinanceUpdateGQLModel) -> FinanceResultGQLModel:
        loader = getLoaders(info).finances
        row = await loader.update(finance)
        result = FinanceResultGQLModel()
        result.msg = "ok"
        result.id = finance.id
        if row is None:
            result.msg = "fail"
            
        return result

    @strawberryA.mutation(description="Adds a new project.")
    async def project_insert(self, info: strawberryA.types.Info, project: ProjectInsertGQLModel) -> ProjectResultGQLModel:
        loader = getLoaders(info).projects
        row = await loader.insert(project)
        result = ProjectResultGQLModel()
        result.msg = "ok"
        result.id = row.id
        return result

    @strawberryA.mutation(description="Update the project.")
    async def project_update(self, info: strawberryA.types.Info, project: ProjectUpdateGQLModel) -> ProjectResultGQLModel:
        loader = getLoaders(info).projects
        row = await loader.update(project)
        result = ProjectResultGQLModel()
        result.msg = "ok"
        result.id = project.id
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

schema = strawberryA.federation.Schema(Query, types=(GroupGQLModel,), mutation=Mutation)
