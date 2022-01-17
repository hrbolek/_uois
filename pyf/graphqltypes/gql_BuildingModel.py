import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class BuildingModelEx(BaseModel):
    __tablename__ = 'buildings'
    __table_args__ = {'extend_existing': True} 
    
    arealmodel = relationship('ArealModelEx')
    # arealmodel = association_proxy('arealmodel', 'keyword')
    roommodels = relationship('RoomModelEx')
    # roommodels = association_proxy('roommodels', 'keyword')


class BuildingModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    lastchange = graphene.DateTime()
    externalId = graphene.String()
    areal_id = graphene.String()
    
        
    arealmodel = graphene.Field('graphqltypes.gql_ArealModel.ArealModel')
    def resolver_arealmodel(parent, info):
        return parent.arealmodel
        
    roommodels = graphene.List('graphqltypes.gql_RoomModel.RoomModel')
        
    def resolver_roommodels(parent, info):
        return parent.roommodels


class create_BuildingModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        externalId = graphene.String(required=True)
        areal_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_BuildingModel.BuildingModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = BuildingModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_BuildingModel(ok=True, result=result)
    pass

class update_BuildingModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)    
        externalId = graphene.String(required=False)    
        areal_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_BuildingModel.BuildingModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(BuildingModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_BuildingModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_buildings_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(BuildingModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_buildings_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(BuildingModelEx).filter(BuildingModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_buildings_lastchange_starts_with(root, info, lastchange):
    try:
        session = extractSession(info)
        dbRecords = session.query(BuildingModelEx).filter(BuildingModel.lastchange.startswith(lastchange)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_buildings_externalId_starts_with(root, info, externalId):
    try:
        session = extractSession(info)
        dbRecords = session.query(BuildingModelEx).filter(BuildingModel.externalId.startswith(externalId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_buildings_areal_id_starts_with(root, info, areal_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(BuildingModelEx).filter(BuildingModel.areal_id.startswith(areal_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords