from uoishelpers.dataloaders import createIdLoader, createFkeyLoader

from gql_ug.DBDefinitions import UserModel, MembershipModel, GroupModel, GroupTypeModel, RoleModel, RoleTypeModel

async def createLoaders(
    asyncSessionMaker,
    DBModels = [UserModel, MembershipModel, GroupModel, GroupTypeModel, RoleModel, RoleTypeModel]
    ):
    
    modelIndex = dict((DBModel.__tablename__, DBModel) for DBModel in DBModels)

    result = {}
    for tableName, DBModel in modelIndex.items():  # iterate over all models
        result[tableName] = createIdLoader(asyncSessionMaker, DBModel)
    #result['memberships'].max_batch_size = 20
    return result

from functools import cache

# async def createLoaders_2(
#     asyncSessionMaker,
#     DBModels = [UserModel, MembershipModel, GroupModel, GroupTypeModel, RoleModel, RoleTypeModel],
#     FKeyedDBModels = {}
#     ):

#     def IdLoader(DBModel):
#         @property
#         @cache
#         def getIt(self):
#             return createIdLoader(asyncSessionMaker, DBModel)

#     def keyedLoader(DBModel, foreignKeyName):
#         @property
#         @cache
#         def getIt(self):
#             return createFkeyLoader(asyncSessionMaker, DBModel, foreignKeyName=foreignKeyName)


#     modelIndex = dict((DBModel.__tablename__, DBModel) for DBModel in DBModels)
#     revIndex = dict((DBModel, DBModel.__tablename__) for DBModel in DBModels)

#     attrs = {}
#     for tableName, DBModel in modelIndex.items():  # iterate over all models
#         attrs[tableName] = IdLoader(DBModel)

#     for DBModel, fkeyNames in FKeyedDBModels.items():
#         tableName = revIndex[DBModel]
#         for fkeyName in fkeyNames:
#             name = tableName + '_' + fkeyName
#             attrs[name] = keyedLoader(DBModel, fkeyName)

#     result = type("loaders", (object, ), attrs)
#     #result = type("resolvers", (object, ), {'experiment': experiment, 'loader_a': experiment})
#     return result()


async def createLoaders_3(asyncSessionMaker):
    class Loaders():
        
        @property
        @cache
        def users(self):
            return createIdLoader(asyncSessionMaker, UserModel)

        @property
        @cache
        def groups(self):
            return createIdLoader(asyncSessionMaker, GroupModel)

        @property
        @cache
        def roles(self):
            return createIdLoader(asyncSessionMaker, RoleModel)

        @property
        @cache
        def roletypes(self):
            return createIdLoader(asyncSessionMaker, RoleTypeModel)

        @property
        @cache
        def grouptypes(self):
            return createIdLoader(asyncSessionMaker, GroupTypeModel)

        @property
        @cache
        def memberships(self):
            return createIdLoader(asyncSessionMaker, MembershipModel)

        @property
        @cache
        def memberships_user_id(self):
            return createFkeyLoader(asyncSessionMaker, MembershipModel, foreignKeyName='user_id')

        @property
        @cache
        def memberships_group_id(self):
            return createFkeyLoader(asyncSessionMaker, MembershipModel, foreignKeyName='group_id')

        @property
        @cache
        def groups_mastergroup_id(self):
            return createFkeyLoader(asyncSessionMaker, GroupModel, foreignKeyName='mastergroup_id')

    return Loaders()