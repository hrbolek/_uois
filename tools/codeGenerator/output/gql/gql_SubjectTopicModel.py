import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class SubjectTopicModel(BaseModel):
    __tablename__ = 'subjecttopics'
    __table_args__ = {'extend_existing': True} 
    
    subjectsemestermodel = relationship('SubjectSemesterModel')
    # subjectsemestermodel = association_proxy('subjectsemestermodel', 'keyword')
    subjecttopicusermodel_collection = relationship('SubjectTopicUserModel')
    # subjecttopicusermodel_collection = association_proxy('subjecttopicusermodel_collection', 'keyword')


class get_SubjectTopicModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    externalId = graphene.String()
    subjectsemester_id = graphene.String()
    
        
    subjectsemestermodel = graphene.Field('gql_SubjectSemesterModel.get_SubjectSemesterModel')
    def resolver_subjectsemestermodel(parent, info):
        return parent.subjectsemestermodel
        
    subjecttopicusermodel_collection = graphene.List('gql_SubjectTopicUserModel.get_SubjectTopicUserModel')
        
    def resolver_subjecttopicusermodel_collection(parent, info):
        return parent.subjecttopicusermodel_collection


class create_SubjectTopicModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        externalId = graphene.String(required=True)
        subjectsemester_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_SubjectTopicModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = SubjectTopicModel(**paramList)
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
    result = graphene.Field('get_SubjectTopicModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(SubjectTopicModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_SubjectTopicModel(ok=True, result=dbRecord)
    pass


def resolve_subjecttopics_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(SubjectTopicModel).filter_by(id=id).one()
    return dbRecord
def resolve_subjecttopics_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(SubjectTopicModel).filter(SubjectTopicModel.name.startswith(name)).all()
    return dbRecords
def resolve_subjecttopics_externalId_starts_with(root, info, externalId):
    session = extractSession(info)
    dbRecords = session.query(SubjectTopicModel).filter(SubjectTopicModel.externalId.startswith(externalId)).all()
    return dbRecords
def resolve_subjecttopics_subjectsemester_id_starts_with(root, info, subjectsemester_id):
    session = extractSession(info)
    dbRecords = session.query(SubjectTopicModel).filter(SubjectTopicModel.subjectsemester_id.startswith(subjectsemester_id)).all()
    return dbRecords