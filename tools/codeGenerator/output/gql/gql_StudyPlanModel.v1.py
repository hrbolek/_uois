import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class StudyPlanModelEx(BaseModel):
    __tablename__ = 'studyplans'
    __table_args__ = {'extend_existing': True} 
    
    studyplanitemmodels = relationship('StudyPlanItemModelEx')
    # studyplanitemmodels = association_proxy('studyplanitemmodels', 'keyword')
    studyplangroupsmodels = relationship('StudyPlanGroupsModelEx')
    # studyplangroupsmodels = association_proxy('studyplangroupsmodels', 'keyword')


class StudyPlanModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    externalId = graphene.String()
    
        
    studyplanitemmodels = graphene.List('graphqltypes.gql_StudyPlanItemModel.StudyPlanItemModel')
        
    def resolver_studyplanitemmodels(parent, info):
        return parent.studyplanitemmodels
        
    studyplangroupsmodels = graphene.List('graphqltypes.gql_StudyPlanGroupsModel.StudyPlanGroupsModel')
        
    def resolver_studyplangroupsmodels(parent, info):
        return parent.studyplangroupsmodels


class create_StudyPlanModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        externalId = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_StudyPlanModel.StudyPlanModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = StudyPlanModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_StudyPlanModel(ok=True, result=result)
    pass

class update_StudyPlanModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        externalId = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_StudyPlanModel.StudyPlanModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(StudyPlanModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_StudyPlanModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_studyplans_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(StudyPlanModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_studyplans_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(StudyPlanModelEx).filter(StudyPlanModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_studyplans_externalId_starts_with(root, info, externalId):
    try:
        session = extractSession(info)
        dbRecords = session.query(StudyPlanModelEx).filter(StudyPlanModel.externalId.startswith(externalId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords