import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class ArealModelEx(BaseModel):
    __tablename__ = 'areals'
    __table_args__ = {'extend_existing': True} 
    
    buildingmodels = relationship('BuildingModelEx')
    # buildingmodels = association_proxy('buildingmodels', 'keyword')


class ArealModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    externalId = graphene.String()
    lastchange = graphene.DateTime()
    
        
    buildingmodels = graphene.List('graphqltypes.gql_BuildingModel.BuildingModel')
        
    def resolver_buildingmodels(parent, info):
        return parent.buildingmodels


class create_ArealModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        externalId = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_ArealModel.ArealModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = ArealModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_ArealModel(ok=True, result=result)
    pass

class update_ArealModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        externalId = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_ArealModel.ArealModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(ArealModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_ArealModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_areals_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(ArealModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_areals_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(ArealModelEx).filter(ArealModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_areals_externalId_starts_with(root, info, externalId):
    try:
        session = extractSession(info)
        dbRecords = session.query(ArealModelEx).filter(ArealModel.externalId.startswith(externalId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_areals_lastchange_starts_with(root, info, lastchange):
    try:
        session = extractSession(info)
        dbRecords = session.query(ArealModelEx).filter(ArealModel.lastchange.startswith(lastchange)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords