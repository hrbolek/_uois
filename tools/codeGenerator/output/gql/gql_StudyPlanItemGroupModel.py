import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class StudyPlanItemGroupModel(BaseModel):
    __tablename__ = 'studyplanitem_groups'
    __table_args__ = {'extend_existing': True} 
    
    studyplanitemmodel = relationship('StudyPlanItemModel')
    # studyplanitemmodel = association_proxy('studyplanitemmodel', 'keyword')
    groupmodel = relationship('GroupModel')
    # groupmodel = association_proxy('groupmodel', 'keyword')


class get_StudyPlanItemGroupModel(graphene.ObjectType):
    
    id = graphene.String()
    group_id = graphene.String()
    studyplanitem_id = graphene.String()
    
        
    studyplanitemmodel = graphene.Field('gql_StudyPlanItemModel.get_StudyPlanItemModel')
    def resolver_studyplanitemmodel(parent, info):
        return parent.studyplanitemmodel
        
    groupmodel = graphene.Field('gql_GroupModel.get_GroupModel')
    def resolver_groupmodel(parent, info):
        return parent.groupmodel


class create_StudyPlanItemGroupModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        group_id = graphene.String(required=True)
        studyplanitem_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_StudyPlanItemGroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = StudyPlanItemGroupModel(**paramList)
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
    result = graphene.Field('get_StudyPlanItemGroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(StudyPlanItemGroupModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_StudyPlanItemGroupModel(ok=True, result=dbRecord)
    pass


def resolve_studyplanitem_groups_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(StudyPlanItemGroupModel).filter_by(id=id).one()
    return dbRecord
def resolve_studyplanitem_groups_group_id_starts_with(root, info, group_id):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanItemGroupModel).filter(StudyPlanItemGroupModel.group_id.startswith(group_id)).all()
    return dbRecords
def resolve_studyplanitem_groups_studyplanitem_id_starts_with(root, info, studyplanitem_id):
    session = extractSession(info)
    dbRecords = session.query(StudyPlanItemGroupModel).filter(StudyPlanItemGroupModel.studyplanitem_id.startswith(studyplanitem_id)).all()
    return dbRecords