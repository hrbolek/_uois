from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, Field, ID, String, List, DateTime, Mutation, Boolean, Int
from graphene import Schema as GSchema

from starlette.graphql import GraphQLApp
#from starlette_graphene import GraphQLApp

import graphene

#import models.BaseEntities as BaseEntities

from contextlib import contextmanager

def attachGraphQL(app, sessionFunc, bindPoint='/gql'):
    """Attaches a Swagger endpoint to a FastAPI

    Parameters
    ----------
    app: FastAPI
        app to bind to
    prepareSession: lambda : session
        callable which returns a db session
    """
    assert callable(sessionFunc), "sessionFunc must be a function creating a session"

    # class Mutations(ObjectType):
    #     create_user = CreateUser.Field()
    #     update_user = UpdateUser.Field()

    def createQueryRoot():

        from graphqltypes.User import UserType, UserRootResolverById
        from graphqltypes.Group import GroupType, GroupRootResolverById, GroupRootResolverByName, resolve_groups_by_type
        from graphqltypes.GroupType import GroupTypeType
        from graphqltypes.Role import RoleType
        from graphqltypes.RoleType import RoleTypeType, RoleTypeRootResolverById, RoleTypeRootResolverByName
        
        from graphqltypes.Event import EventType
        from graphqltypes.StudyPlan import StudyPlanType, StudyPlanRootResolverById

        from graphqltypes.Program import ProgramType, ProgramRootResolverById
        from graphqltypes.Subject import SubjectType, SubjectRootResolverById, SubjectRootResolverByName
        from graphqltypes.SubjectSemester import SubjectSemesterType, SubjectSemesterRootResolverById, SubjectSemesterRootResolverByName


        from graphqltypes.Areal import ArealType, CreateRandomAreal, ArealRootResolverById, ArealRootResolverByName
        from graphqltypes.Building import BuildingType, BuildingRootResolverById, BuildingRootResolverByName
        from graphqltypes.Room import RoomType, RoomRootResolverById, RoomRootResolverByName


        class QueryRoot(ObjectType):
            user = Field(UserType, id=ID(required=True), resolver=UserRootResolverById)
            group = Field(GroupType, id=ID(required=True), resolver=GroupRootResolverById)
            group_by_name = Field(GroupType, name=String(required=True), resolver=GroupRootResolverByName)
            groups_by_type = Field(List(GroupType), type_id=Int(required=True), resolver=resolve_groups_by_type)
            roletype = Field(RoleTypeType, id=ID(required=True), resolver=RoleTypeRootResolverById)
            roletype_by_name = Field(RoleTypeType, name=String(required=True), resolver=RoleTypeRootResolverByName)
            
            areal = Field(ArealType, id=ID(required=True), resolver=ArealRootResolverById)
            areal_by_name = Field(ArealType, name=String(required=True), resolver=ArealRootResolverByName)
            building = Field(BuildingType, id=ID(required=True), resolver=BuildingRootResolverById)
            building_by_name = Field(BuildingType, name=String(required=True), resolver=BuildingRootResolverByName)
            room = Field(RoomType, id=ID(required=True), resolver=RoomRootResolverById)
            room_by_name = Field(RoomType, name=String(required=True), resolver=RoomRootResolverByName)
            
            program = Field(ProgramType, id=ID(required=True), resolver=ProgramRootResolverById)
            subject = Field(SubjectType, id=ID(required=True), resolver=SubjectRootResolverById)
            subject_semester = Field(SubjectSemesterType, id=ID(required=True), resolver=SubjectSemesterRootResolverById)
            study_plan = Field(StudyPlanType, id=ID(required=True), resolver=StudyPlanRootResolverById)


        return QueryRoot

    def createMutationRoot():

        from graphqltypes.Areal import ArealType, CreateRandomAreal
        from graphqltypes.Group import CreateRandomUniversity
        from graphqltypes.Program import CreateRandomProgram
        from graphqltypes.StudyPlan import CreateStudyPlan

        class MutationRoot(ObjectType):
            create_random_areal = CreateRandomAreal.Field()
            create_random_university = CreateRandomUniversity.Field()
            create_random_program = CreateRandomProgram.Field()

            create_study_plan = CreateStudyPlan.Field()

        return MutationRoot

    #router = fastapi.APIRouter()
    #https://github.com/graphql-python/graphene-sqlalchemy/issues/292
    #router = APIRouter()

    session_scope = contextmanager(sessionFunc)

    # class SessionMiddleware(object):
    #     # this does not work because of default resolvers
    #     def resolve(self, next, root, info, **args):
    #         print('SessionMiddleware Action')
    #         with session_scope() as session:
    #             print('info.context', info.context)
    #             info.context['session'] = session
    #             print('query for', args.keys())
    #             return next(root, info, **args)

    class localSchema(graphene.Schema):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

        def execute(self, *args, **kwargs):
            with session_scope() as session:
                if 'context' in kwargs:
                    newkwargs = {**kwargs, 'context': {**kwargs['context'], 'session': session}}
                else:
                    newkwargs = {**kwargs, 'context': {'session': session}}
                return super().execute(*args, **newkwargs)

        async def execute_async(self, *args, **kwargs):
            with session_scope() as session:
                if 'context' in kwargs:
                    newkwargs = {**kwargs, 'context': {**kwargs['context'], 'session': session}}
                else:
                    newkwargs = {**kwargs, 'context': {'session': session}}
                return await super().execute_async(*args, **newkwargs)



    #graphql_app = GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutations), context_value={'session': None})#, middleware=[SessionMiddleware()])
    #app.add_route("/gql/", graphql_app)
    
    #graphql_app = GraphQLApp(schema=localSchema(query=Query, mutation=Mutations))
    #graphql_app = GraphQLApp(schema=localSchema(query=createQueryRoot(), mutation=Mutations))
    graphql_app = GraphQLApp(schema=localSchema(query=createQueryRoot(), mutation=createMutationRoot()))
    
    app.add_route(bindPoint, graphql_app)

