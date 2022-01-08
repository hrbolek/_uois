import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class AcreditationUserRoleTypeModel(BaseModel):
    __tablename__ = 'acreditationuserroletypes'
    __table_args__ = {'extend_existing': True} 
    
    programusermodel_collection = relationship('ProgramUserModel')
    # programusermodel_collection = association_proxy('programusermodel_collection', 'keyword')
    subjectusermodel_collection = relationship('SubjectUserModel')
    # subjectusermodel_collection = association_proxy('subjectusermodel_collection', 'keyword')
    subjecttopicusermodel_collection = relationship('SubjectTopicUserModel')
    # subjecttopicusermodel_collection = association_proxy('subjecttopicusermodel_collection', 'keyword')


class get_AcreditationUserRoleTypeModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    
        
    programusermodel_collection = graphene.List('gql_ProgramUserModel.get_ProgramUserModel')
        
    def resolver_programusermodel_collection(parent, info):
        return parent.programusermodel_collection
        
    subjectusermodel_collection = graphene.List('gql_SubjectUserModel.get_SubjectUserModel')
        
    def resolver_subjectusermodel_collection(parent, info):
        return parent.subjectusermodel_collection
        
    subjecttopicusermodel_collection = graphene.List('gql_SubjectTopicUserModel.get_SubjectTopicUserModel')
        
    def resolver_subjecttopicusermodel_collection(parent, info):
        return parent.subjecttopicusermodel_collection


class create_AcreditationUserRoleTypeModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_AcreditationUserRoleTypeModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = AcreditationUserRoleTypeModel(**paramList)
        session.add(result)
        session.commit()
        return create_AcreditationUserRoleTypeModel(ok=True, result=result)
    pass

class update_AcreditationUserRoleTypeModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_AcreditationUserRoleTypeModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(AcreditationUserRoleTypeModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_AcreditationUserRoleTypeModel(ok=True, result=dbRecord)
    pass


def resolve_acreditationuserroletypes_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(AcreditationUserRoleTypeModel).filter_by(id=id).one()
    return dbRecord
def resolve_acreditationuserroletypes_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(AcreditationUserRoleTypeModel).filter(AcreditationUserRoleTypeModel.name.startswith(name)).all()
    return dbRecords