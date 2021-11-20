from typing import List, Optional

import strawberry
from strawberry.fastapi import GraphQLRouter
from sqlalchemy import select
from starlette.applications import Starlette
from strawberry.asgi import GraphQL

import models


def attachGraphQL(app, sessionFunc):


    @strawberry.type
    class Location:
        id: strawberry.ID
        name: str

        @classmethod
        def marshal(cls, model: models.Location) -> "Location":
            return cls(id=strawberry.ID(str(model.id)), name=model.name)


    @strawberry.type
    class Task:
        id: strawberry.ID
        name: str
        location: Optional[Location] = None

        @classmethod
        def marshal(cls, model: models.Task) -> "Task":
            return cls(
                id=strawberry.ID(str(model.id)),
                name=model.name,
                location=Location.marshal(model.location) if model.location else None,
            )


    # @strawberry.type
    # class LocationNotFound:
    #     message: str = "Location with this name does not exist"


    AddTaskResponse = strawberry.union("AddTaskResponse", (Task,))


    @strawberry.type
    class LocationExists:
        message: str = "Location with this name already exist"


    AddLocationResponse = strawberry.union("AddLocationResponse", (Location, LocationExists))


    @strawberry.type
    class Mutation:
        @strawberry.mutation
        async def add_task(self, name: str, location_name: Optional[str]) -> AddTaskResponse:
            async with sessionFunc() as session:
                db_location = None
                if location_name:
                    sql = select(models.Location).where(models.Location.name == location_name)
                    db_location = (await session.execute(sql)).scalars().first()
                    # if db_location is None:
                    #     return LocationNotFound()
                db_task = models.Task(name=name, location=db_location)
                session.add(db_task)
                await session.commit()
            return Task.marshal(db_task)

        @strawberry.mutation
        async def add_location(self, name: str) -> AddLocationResponse:
            async with sessionFunc() as session:
                sql = select(models.Location).where(models.Location.name == name)
                existing_db_location = (await session.execute(sql)).first()
                if existing_db_location is not None:
                    return LocationExists()
                db_location = models.Location(name=name)
                session.add(db_location)
                await session.commit()
            return Location.marshal(db_location)


    @strawberry.type
    class Query:
        @strawberry.field
        async def tasks(self) -> List[Task]:
            async with sessionFunc() as session:
                sql = select(models.Task).order_by(models.Task.name)
                db_tasks = (await session.execute(sql)).scalars().unique().all()
            return [Task.marshal(task) for task in db_tasks]

        @strawberry.field
        async def locations(self) -> List[Location]:
            async with sessionFunc() as session:
                sql = select(models.Location).order_by(models.Location.name)
                db_locations = (await session.execute(sql)).scalars().unique().all()
            return [Location.marshal(loc) for loc in db_locations]


    # @strawberry.type
    # class Query:
    #     @strawberry.field
    #     def hello(self) -> str:
    #         return "Hello World"


    schema = strawberry.Schema(Query)

    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphqlstr")   
    pass