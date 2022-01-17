import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class SubjectTopicModelEx(BaseModel):
    __tablename__ = 'subjecttopics'
    __table_args__ = {'extend_existing': True} 
    
    subjectsemestermodel = relationship('SubjectSemesterModelEx')
    # subjectsemestermodel = association_proxy('subjectsemestermodel', 'keyword')
    subjecttopicusermodels = relationship('SubjectTopicUserModelEx')
    # subjecttopicusermodels = association_proxy('subjecttopicusermodels', 'keyword')


class SubjectTopicModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    externalId = graphene.String()
    subjectsemester_id = graphene.String()
    
        
    subjectsemestermodel = graphene.Field('graphqltypes.gql_SubjectSemesterModel.SubjectSemesterModel')
    def resolver_subjectsemestermodel(parent, info):
        return parent.subjectsemestermodel
        
    subjecttopicusermodels = graphene.List('graphqltypes.gql_SubjectTopicUserModel.SubjectTopicUserModel')
        
    def resolver_subjecttopicusermodels(parent, info):
        return parent.subjecttopicusermodels


class create_SubjectTopicModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        externalId = graphene.String(required=True)
        subjectsemester_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_SubjectTopicModel.SubjectTopicModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = SubjectTopicModelEx(**paramList)
        session.add(result)
        session.commit()
        return create_SubjectTopicModel(ok=True, result=result)
    pass

class update_SubjectTopicModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        externalId = graphene.String(required=False)    
        subjectsemester_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('graphqltypes.gql_SubjectTopicModel.SubjectTopicModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(SubjectTopicModelEx).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_SubjectTopicModel(ok=True, result=dbRecord)
    pass

def to_dict(row):
    return {column.name: getattr(row, row.__mapper__.get_property_by_column(column).key) for column in row.__table__.columns}


def resolve_subjecttopics_by_id(root, info, id):
    try:
        session = extractSession(info)
        dbRecord = session.query(SubjectTopicModelEx).filter_by(id=id).one()
    except Exception as e:
        print('An error occured (by_id)')
        print(e)
    print(f'to_dict(dbRecord)')
    return dbRecord
def resolve_subjecttopics_name_starts_with(root, info, name):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectTopicModelEx).filter(SubjectTopicModel.name.startswith(name)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_subjecttopics_externalId_starts_with(root, info, externalId):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectTopicModelEx).filter(SubjectTopicModel.externalId.startswith(externalId)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords
def resolve_subjecttopics_subjectsemester_id_starts_with(root, info, subjectsemester_id):
    try:
        session = extractSession(info)
        dbRecords = session.query(SubjectTopicModelEx).filter(SubjectTopicModel.subjectsemester_id.startswith(subjectsemester_id)).all()
    except Exception as e:
        print('An error occured (startswith)')
        print(e)
    return dbRecords