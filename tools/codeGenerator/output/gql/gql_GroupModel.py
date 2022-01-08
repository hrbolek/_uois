import graphene
from sqlalchemy.orm import relationship
from BaseModel import BaseModel

def extractSession(info):
    #return info.context['request'].scope['db_session']
    assert not info.context is None, 'Got Bad Context'
    return info.context.get('session')

class GroupModel(BaseModel):
    __tablename__ = 'groups'
    __table_args__ = {'extend_existing': True} 
    
    grouptypemodel = relationship('GroupTypeModel')
    # grouptypemodel = association_proxy('grouptypemodel', 'keyword')
    groupconnectionmodel_collection = relationship('GroupConnectionModel')
    # groupconnectionmodel_collection = association_proxy('groupconnectionmodel_collection', 'keyword')
    usergroupmodel_collection = relationship('UserGroupModel')
    # usergroupmodel_collection = association_proxy('usergroupmodel_collection', 'keyword')
    rolemodel_collection = relationship('RoleModel')
    # rolemodel_collection = association_proxy('rolemodel_collection', 'keyword')
    eventgroupmodel_collection = relationship('EventGroupModel')
    # eventgroupmodel_collection = association_proxy('eventgroupmodel_collection', 'keyword')
    studyplangroupsmodel_collection = relationship('StudyPlanGroupsModel')
    # studyplangroupsmodel_collection = association_proxy('studyplangroupsmodel_collection', 'keyword')
    studyplanitemgroupmodel_collection = relationship('StudyPlanItemGroupModel')
    # studyplanitemgroupmodel_collection = association_proxy('studyplanitemgroupmodel_collection', 'keyword')


class get_GroupModel(graphene.ObjectType):
    
    id = graphene.String()
    name = graphene.String()
    abbreviation = graphene.String()
    lastchange = graphene.DateTime()
    entryYearId = graphene.Int()
    externalId = graphene.String()
    UIC = graphene.String()
    grouptype_id = graphene.String()
    
        
    grouptypemodel = graphene.Field('gql_GroupTypeModel.get_GroupTypeModel')
    def resolver_grouptypemodel(parent, info):
        return parent.grouptypemodel
        
    groupconnectionmodel_collection = graphene.List('gql_GroupConnectionModel.get_GroupConnectionModel')
        
    def resolver_groupconnectionmodel_collection(parent, info):
        return parent.groupconnectionmodel_collection
        
    usergroupmodel_collection = graphene.List('gql_UserGroupModel.get_UserGroupModel')
        
    def resolver_usergroupmodel_collection(parent, info):
        return parent.usergroupmodel_collection
        
    rolemodel_collection = graphene.List('gql_RoleModel.get_RoleModel')
        
    def resolver_rolemodel_collection(parent, info):
        return parent.rolemodel_collection
        
    eventgroupmodel_collection = graphene.List('gql_EventGroupModel.get_EventGroupModel')
        
    def resolver_eventgroupmodel_collection(parent, info):
        return parent.eventgroupmodel_collection
        
    studyplangroupsmodel_collection = graphene.List('gql_StudyPlanGroupsModel.get_StudyPlanGroupsModel')
        
    def resolver_studyplangroupsmodel_collection(parent, info):
        return parent.studyplangroupsmodel_collection
        
    studyplanitemgroupmodel_collection = graphene.List('gql_StudyPlanItemGroupModel.get_StudyPlanItemGroupModel')
        
    def resolver_studyplanitemgroupmodel_collection(parent, info):
        return parent.studyplanitemgroupmodel_collection


class create_GroupModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)
        abbreviation = graphene.String(required=True)
        lastchange = graphene.DateTime(required=True)
        entryYearId = graphene.Int(required=True)
        externalId = graphene.String(required=True)
        UIC = graphene.String(required=True)
        grouptype_id = graphene.String(required=True)

    ok = graphene.Boolean()
    result = graphene.Field('get_GroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = GroupModel(**paramList)
        session.add(result)
        session.commit()
        return create_GroupModel(ok=True, result=result)
    pass

class update_GroupModel(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)    
        name = graphene.String(required=False)    
        abbreviation = graphene.String(required=False)    
        lastchange = graphene.DateTime(required=False)    
        entryYearId = graphene.Int(required=False)    
        externalId = graphene.String(required=False)    
        UIC = graphene.String(required=False)    
        grouptype_id = graphene.String(required=False)

    ok = graphene.Boolean()
    result = graphene.Field('get_GroupModel')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query(GroupModel).filter_by(id=paramList['id']).one()
        for key, item in paramList.items():
            if key=='id':
                continue
            setattr(dbRecord, key, item)
        session.commit()
        return update_GroupModel(ok=True, result=dbRecord)
    pass


def resolve_groups_by_id(root, info, id):
    session = extractSession(info)
    dbRecord = session.query(GroupModel).filter_by(id=id).one()
    return dbRecord
def resolve_groups_name_starts_with(root, info, name):
    session = extractSession(info)
    dbRecords = session.query(GroupModel).filter(GroupModel.name.startswith(name)).all()
    return dbRecords
def resolve_groups_abbreviation_starts_with(root, info, abbreviation):
    session = extractSession(info)
    dbRecords = session.query(GroupModel).filter(GroupModel.abbreviation.startswith(abbreviation)).all()
    return dbRecords
def resolve_groups_lastchange_starts_with(root, info, lastchange):
    session = extractSession(info)
    dbRecords = session.query(GroupModel).filter(GroupModel.lastchange.startswith(lastchange)).all()
    return dbRecords
def resolve_groups_entryYearId_starts_with(root, info, entryYearId):
    session = extractSession(info)
    dbRecords = session.query(GroupModel).filter(GroupModel.entryYearId.startswith(entryYearId)).all()
    return dbRecords
def resolve_groups_externalId_starts_with(root, info, externalId):
    session = extractSession(info)
    dbRecords = session.query(GroupModel).filter(GroupModel.externalId.startswith(externalId)).all()
    return dbRecords
def resolve_groups_UIC_starts_with(root, info, UIC):
    session = extractSession(info)
    dbRecords = session.query(GroupModel).filter(GroupModel.UIC.startswith(UIC)).all()
    return dbRecords
def resolve_groups_grouptype_id_starts_with(root, info, grouptype_id):
    session = extractSession(info)
    dbRecords = session.query(GroupModel).filter(GroupModel.grouptype_id.startswith(grouptype_id)).all()
    return dbRecords