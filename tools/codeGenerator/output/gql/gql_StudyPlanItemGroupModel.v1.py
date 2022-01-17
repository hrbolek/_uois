import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class StudyPlanItemGroupModelEx(BaseModel):
    __tablename__ = 'studyplanitem_groups'
    __table_args__ = {'extend_existing': True} 
    
    studyplanitemmodel = relationship('StudyPlanItemModelEx')
    # studyplanitemmodel = association_proxy('studyplanitemmodel', 'keyword')
    groupmodel = relationship('GroupModelEx')
    # groupmodel = association_proxy('groupmodel', 'keyword')


class StudyPlanItemGroupModel(graphene.ObjectType):
    
    id = graphene.String()
    group_id = graphene.String()
    studyplanitem_id = graphene.String()
    
        
    studyplanitemmodel = graphene.Field('graphqltypes.gql_StudyPlanItemModel.StudyPlanItemModel')
    def resolver_studyplanitemmodel(parent, info):
        return parent.studyplanitemmodel
        
    groupmodel = graphene.Field('graphqltypes.gql_GroupModel.GroupModel')
    def resolver_groupmodel(parent, info):
        return parent.groupmodel


class create_StudyPlanItemGroupModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        group_id = graphene.String(required=True)
        studyplanitem_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_StudyPlanItemGroupModel.StudyPlanItemGroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = StudyPlanItemGroupModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_StudyPlanItemGroupModel(ok=True, result=result)
    pass

class update_StudyPlanItemGroupModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        group_id = graphene.String(required=False)    
        studyplanitem_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_StudyPlanItemGroupModel.StudyPlanItemGroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(StudyPlanItemGroupModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_StudyPlanItemGroupModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_studyplanitem_groups_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(StudyPlanItemGroupModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_studyplanitem_groups_group_id_starts_with(root, info, group_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(StudyPlanItemGroupModelEx).filter(StudyPlanItemGroupModel.group_id.startswith(group_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_studyplanitem_groups_studyplanitem_id_starts_with(root, info, studyplanitem_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(StudyPlanItemGroupModelEx).filter(StudyPlanItemGroupModel.studyplanitem_id.startswith(studyplanitem_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords