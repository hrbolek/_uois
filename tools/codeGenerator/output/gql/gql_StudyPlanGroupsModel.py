import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class StudyPlanGroupsModel(BaseModel):
    __tablename__ = 'studyplans_groups'
    __table_args__ = {'extend_existing': True} 
    
    groupmodel = relationship('GroupModel')
    # groupmodel = association_proxy('groupmodel', 'keyword')
    studyplanmodel = relationship('StudyPlanModel')
    # studyplanmodel = association_proxy('studyplanmodel', 'keyword')


class get_StudyPlanGroupsModel(graphene.ObjectType):
    
    id = graphene.String()
    studyplan_id = graphene.String()
    group_id = graphene.String()
    
        
    groupmodel = graphene.Field('gql_GroupModel.get_GroupModel')
    def resolver_groupmodel(parent, info):
        return parent.groupmodel
        
    studyplanmodel = graphene.Field('gql_StudyPlanModel.get_StudyPlanModel')
    def resolver_studyplanmodel(parent, info):
        return parent.studyplanmodel


class create_StudyPlanGroupsModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        studyplan_id = graphene.String(required=True)
        group_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_StudyPlanGroupsModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = StudyPlanGroupsModel(**paramList)
        session.add(result)
        session.commit()
        return create_StudyPlanGroupsModel(ok=True, result=result)
    pass

class update_StudyPlanGroupsModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        studyplan_id = graphene.String(required=False)    
        group_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_StudyPlanGroupsModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(StudyPlanGroupsModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_StudyPlanGroupsModel(ok=True, result=dbRecord)
    pass


def resolve_studyplans_groups_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(StudyPlanGroupsModel).filter_by(id=id).one()
    return dbRecord
def resolve_studyplans_groups_studyplan_id_starts_with(root, info, studyplan_id):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanGroupsModel).filter(StudyPlanGroupsModel.studyplan_id.startswith(studyplan_id)).all()
    return dbRecords
def resolve_studyplans_groups_group_id_starts_with(root, info, group_id):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanGroupsModel).filter(StudyPlanGroupsModel.group_id.startswith(group_id)).all()
    return dbRecords