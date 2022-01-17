import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class StudyPlanGroupsModelEx(BaseModel):
    __tablename__ = 'studyplans_groups'
    __table_args__ = {'extend_existing': True} 
    
    groupmodel = relationship('GroupModelEx')
    # groupmodel = association_proxy('groupmodel', 'keyword')
    studyplanmodel = relationship('StudyPlanModelEx')
    # studyplanmodel = association_proxy('studyplanmodel', 'keyword')


class StudyPlanGroupsModel(graphene.ObjectType):
    
    id = graphene.String()
    studyplan_id = graphene.String()
    group_id = graphene.String()
    
        
    groupmodel = graphene.Field('graphqltypes.gql_GroupModel.GroupModel')
    def resolver_groupmodel(parent, info):
        return parent.groupmodel
        
    studyplanmodel = graphene.Field('graphqltypes.gql_StudyPlanModel.StudyPlanModel')
    def resolver_studyplanmodel(parent, info):
        return parent.studyplanmodel


class create_StudyPlanGroupsModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        studyplan_id = graphene.String(required=True)
        group_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_StudyPlanGroupsModel.StudyPlanGroupsModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = StudyPlanGroupsModelEx(**paramList)
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
    result = graphene.Field('graphqltypes.gql_StudyPlanGroupsModel.StudyPlanGroupsModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(StudyPlanGroupsModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_StudyPlanGroupsModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_studyplans_groups_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(StudyPlanGroupsModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_studyplans_groups_studyplan_id_starts_with(root, info, studyplan_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(StudyPlanGroupsModelEx).filter(StudyPlanGroupsModel.studyplan_id.startswith(studyplan_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_studyplans_groups_group_id_starts_with(root, info, group_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(StudyPlanGroupsModelEx).filter(StudyPlanGroupsModel.group_id.startswith(group_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords