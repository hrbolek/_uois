import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class StudyPlanModel(BaseModel):
    __tablename__ = 'studyplans'
    __table_args__ = {'extend_existing': True} 
    
    studyplanitemmodel_collection = relationship('StudyPlanItemModel')
    # studyplanitemmodel_collection = association_proxy('studyplanitemmodel_collection', 'keyword')
    studyplangroupsmodel_collection = relationship('StudyPlanGroupsModel')
    # studyplangroupsmodel_collection = association_proxy('studyplangroupsmodel_collection', 'keyword')


class get_StudyPlanModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    externalId = graphene.String()
    
        
    studyplanitemmodel_collection = graphene.List('gql_StudyPlanItemModel.get_StudyPlanItemModel')
        
    def resolver_studyplanitemmodel_collection(parent, info):
        return parent.studyplanitemmodel_collection
        
    studyplangroupsmodel_collection = graphene.List('gql_StudyPlanGroupsModel.get_StudyPlanGroupsModel')
        
    def resolver_studyplangroupsmodel_collection(parent, info):
        return parent.studyplangroupsmodel_collection


class create_StudyPlanModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        externalId = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_StudyPlanModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = StudyPlanModel(**paramList)
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
    result = graphene.Field('get_StudyPlanModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(StudyPlanModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_StudyPlanModel(ok=True, result=dbRecord)
    pass


def resolve_studyplans_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(StudyPlanModel).filter_by(id=id).one()
    return dbRecord
def resolve_studyplans_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanModel).filter(StudyPlanModel.name.startswith(name)).all()
    return dbRecords
def resolve_studyplans_externalId_starts_with(root, info, externalId):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanModel).filter(StudyPlanModel.externalId.startswith(externalId)).all()
    return dbRecords