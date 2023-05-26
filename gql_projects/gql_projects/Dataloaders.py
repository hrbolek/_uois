from uoishelpers.dataloaders import createIdLoader, createFkeyLoader

from gql_projects.DBDefinitions import (
    ProjectCategoryModel,
    ProjectTypeModel,
    ProjectModel,
    MilestoneModel,
    MilestoneLinkModel,
    FinanceCategory,
    FinanceTypeModel,
    FinanceModel
)


dbmodels = {
    "projectcategories": ProjectCategoryModel,
    "projecttypes": ProjectTypeModel,
    "projects": ProjectModel,
    "milestones": MilestoneModel,
    "milestonelinks": MilestoneLinkModel,
    "financecategory": FinanceCategory,
    "financetypes": FinanceTypeModel,
    "finances": FinanceModel
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