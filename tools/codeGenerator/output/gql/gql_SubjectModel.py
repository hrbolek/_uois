import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class SubjectModel(BaseModel):
    __tablename__ = 'subjects'
    __table_args__ = {'extend_existing': True} 
    
    programmodel = relationship('ProgramModel')
    # programmodel = association_proxy('programmodel', 'keyword')
    subjectusermodel_collection = relationship('SubjectUserModel')
    # subjectusermodel_collection = association_proxy('subjectusermodel_collection', 'keyword')
    subjectsemestermodel_collection = relationship('SubjectSemesterModel')
    # subjectsemestermodel_collection = association_proxy('subjectsemestermodel_collection', 'keyword')


class get_SubjectModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    lastchange = graphene.DateTime()
    externalId = graphene.String()
    program_id = graphene.String()
    
        
    programmodel = graphene.Field('gql_ProgramModel.get_ProgramModel')
    def resolver_programmodel(parent, info):
        return parent.programmodel
        
    subjectusermodel_collection = graphene.List('gql_SubjectUserModel.get_SubjectUserModel')
        
    def resolver_subjectusermodel_collection(parent, info):
        return parent.subjectusermodel_collection
        
    subjectsemestermodel_collection = graphene.List('gql_SubjectSemesterModel.get_SubjectSemesterModel')
        
    def resolver_subjectsemestermodel_collection(parent, info):
        return parent.subjectsemestermodel_collection


class create_SubjectModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        externalId = graphene.String(required=True)
        program_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_SubjectModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = SubjectModel(**paramList)
        session.add(result)
        session.commit()
        return create_SubjectModel(ok=True, result=result)
    pass

class update_SubjectModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)    
        externalId = graphene.String(required=False)    
        program_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_SubjectModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(SubjectModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_SubjectModel(ok=True, result=dbRecord)
    pass


def resolve_subjects_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(SubjectModel).filter_by(id=id).one()
    return dbRecord
def resolve_subjects_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(SubjectModel).filter(SubjectModel.name.startswith(name)).all()
    return dbRecords
def resolve_subjects_lastchange_starts_with(root, info, lastchange):
    session = extractSession(info)
    dbRecords = session.query(SubjectModel).filter(SubjectModel.lastchange.startswith(lastchange)).all()
    return dbRecords
def resolve_subjects_externalId_starts_with(root, info, externalId):
    session = extractSession(info)
    dbRecords = session.query(SubjectModel).filter(SubjectModel.externalId.startswith(externalId)).all()
    return dbRecords
def resolve_subjects_program_id_starts_with(root, info, program_id):
    session = extractSession(info)
    dbRecords = session.query(SubjectModel).filter(SubjectModel.program_id.startswith(program_id)).all()
    return dbRecords