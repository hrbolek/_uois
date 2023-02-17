from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from functools import cache

from gql_externalids.DBDefinitions import ExternalIdModel, ExternalIdTypeModel, ExternalIdCategoryModel
async def createLoaders_3(asyncSessionMaker):

    class Loaders:
        @property
        @cache
        def externalids(self):
            return createIdLoader(asyncSessionMaker, ExternalIdModel)

        @property
        @cache
        def externaltypeids(self):
            return createIdLoader(asyncSessionMaker, ExternalIdTypeModel)

        @property
        @cache
        def externalcategoryids(self):
            return createIdLoader(asyncSessionMaker, ExternalIdCategoryModel)

        @property
        @cache
        def externalids_inner_id(self):
            return createFkeyLoader(
                asyncSessionMaker, ExternalIdModel, foreignKeyName="inner_id"
            )

    return Loaders()
