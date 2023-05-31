from uoishelpers.dataloaders import createIdLoader, createFkeyLoader

from gql_lessons.DBDefinitions import (
    PlanModel,
    PlannedLessonModel,
    UserPlanModel,
    GroupPlanModel,
    FacilityPlanModel
)


dbmodels = {
    "psps": PlanModel,
    "plans": PlannedLessonModel,
    "userplans": UserPlanModel,
    "groupplans": GroupPlanModel,
    "facilityplans": FacilityPlanModel
}

async def createLoaders(asyncSessionMaker, models=dbmodels):
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

from functools import cache