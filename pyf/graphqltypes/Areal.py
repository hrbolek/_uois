from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int

from models.FacilitiesRelated.ArealModel import ArealModel
from models.FacilitiesRelated.BuildingModel import BuildingModel
from graphqltypes.Utils import extractSession

class ArealType(ObjectType):
    id = ID()

    lastchange = DateTime()
    externalId = String()

    buildings = Field('graphqltypes.Building.BuildingType')

    def resolve_buildings(parent, info):
        session = extractSession(info)
        dbRecords = session.query(BuildingModel).filter(BuildingModel.areal_id == parent.id).all()
        return dbRecords
        

