import random
from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int

from models.FacilitiesRelated.ArealModel import ArealModel
from models.FacilitiesRelated.BuildingModel import BuildingModel
from models.FacilitiesRelated.RoomModel import RoomModel
from graphqltypes.Utils import extractSession

from graphqltypes.Utils import createRootResolverById, createRootResolverByName

ArealRootResolverById = createRootResolverById(ArealModel)
ArealRootResolverByName = createRootResolverByName(ArealModel)


class ArealType(ObjectType):
    id = ID()

    lastchange = DateTime()
    externalId = String()
    name = String()

    buildings = List('graphqltypes.Building.BuildingType')

    def resolve_buildings(parent, info):
        if hasattr(parent, 'buildings'):
            result = parent.buildings
        else:
            session = extractSession(info)
            result = session.query(BuildingModel).filter(BuildingModel.areal_id == parent.id).all()
        return result
        

class CreateRandomAreal(Mutation):
    class Arguments():
        buildingCount = Int()
        name = String()
        pass

    result = Field('graphqltypes.Areal.ArealType')
    ok = Boolean()

    def mutate(root, info, name='K', buildingCount=5):
        session = extractSession(info)

        def randomRoom(building, prefix, floor, index):
            dbRecord = RoomModel(name=f'{prefix}/{floor}-{index}', building=building)
            session.add(dbRecord)
            session.commit()
            return dbRecord

        def randomBuilding(areal, index):
            floorCount = random.randrange(2, 5)
            roomCount = random.randrange(10, 20)
            prefix = f'{areal.name}/{index}'
            dbRecord = BuildingModel(name=prefix)
            session.add(dbRecord)
            session.commit()

            for x in range(floorCount):
                for y in range(roomCount):
                    randomRoom(dbRecord, prefix, x+1, y+1).building = dbRecord
            return dbRecord

        try:
            result = ArealModel(name=name)
            session.add(result)
            session.commit()
            for i in range(buildingCount):
                randomBuilding(result, i+1).areal = result
            session.commit()
        except Exception as e:
            print(e)

        return CreateRandomAreal(ok=True, result=result)
    pass