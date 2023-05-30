import datetime
from functools import cache
from aiodataloader import DataLoader
from sqlalchemy import select, update

from uoishelpers.dataloaders import createIdLoader

from gql_preferences.DBDefinitions import (
    TagModel, TagEntityModel
)

dbmodels = {
    "tags": TagModel,
    "tagentities" : TagEntityModel
}

def createDataLoders(asyncSessionMaker, models=dbmodels):
    result = createLoaders(asyncSessionMaker, models)
    return result


async def createLoaders(asyncSessionMaker, models=dbmodels):
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

from functools import cache