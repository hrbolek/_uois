import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class ProgramModel(BaseModel):
    __tablename__ = 'programs'
    __table_args__ = {'extend_existing': True} 
    
    programusermodel_collection = relationship('ProgramUserModel')
    # programusermodel_collection = association_proxy('programusermodel_collection', 'keyword')
    subjectmodel_collection = relationship('SubjectModel')
    # subjectmodel_collection = association_proxy('subjectmodel_collection', 'keyword')


class get_ProgramModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    lastchange = graphene.DateTime()
    externalId = graphene.Int()
    
        
    programusermodel_collection = graphene.List('gql_ProgramUserModel.get_ProgramUserModel')
        
    def resolver_programusermodel_collection(parent, info):
        return parent.programusermodel_collection
        
    subjectmodel_collection = graphene.List('gql_SubjectModel.get_SubjectModel')
        
    def resolver_subjectmodel_collection(parent, info):
        return parent.subjectmodel_collection


class create_ProgramModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        externalId = graphene.Int(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_ProgramModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = ProgramModel(**paramList)
        session.add(result)
        session.commit()
        return create_ProgramModel(ok=True, result=result)
    pass

class update_ProgramModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)    
        externalId = graphene.Int(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_ProgramModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(ProgramModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_ProgramModel(ok=True, result=dbRecord)
    pass


def resolve_programs_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(ProgramModel).filter_by(id=id).one()
    return dbRecord
def resolve_programs_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(ProgramModel).filter(ProgramModel.name.startswith(name)).all()
    return dbRecords
def resolve_programs_lastchange_starts_with(root, info, lastchange):
    session = extractSession(info)
    dbRecords = session.query(ProgramModel).filter(ProgramModel.lastchange.startswith(lastchange)).all()
    return dbRecords
def resolve_programs_externalId_starts_with(root, info, externalId):
    session = extractSession(info)
    dbRecords = session.query(ProgramModel).filter(ProgramModel.externalId.startswith(externalId)).all()
    return dbRecords