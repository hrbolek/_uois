from typing_extensions import Required

#from sqlalchemy.sql.sqltypes import Boolean
from graphene import ObjectType, String, Field, ID, List, DateTime, Mutation, Boolean, Int

from models.GroupRelated.UserModel import UserModel
from models.GroupRelated.UserGroupModel import UserGroupModel
from graphqltypes.Utils import extractSession
from models.GroupRelated.GroupModel import GroupModel

from graphqltypes.Group import GroupType

from graphqltypes.Utils import createRootResolverById, createRootResolverByName

UserRootResolverById = createRootResolverById(UserModel)

class UserType(ObjectType):
    id = ID()
    name = String()
    surname = String()
    email = String()

    #lastchange = DateTime()
    #externalId = String()

    groups = List('graphqltypes.Group.GroupType')
    #groups = List(lambda: GroupType)
    def resolve_groups(parent, info):
        session = extractSession(info)
        dbRecords = session.query(UserModel).filter_by(id=parent.id).first()
        return dbRecords.groups


    groups_by_type = List('graphqltypes.Group.GroupType', type_id=Int(required=True))
    def resolve_groups_by_type(parent, info, type_id):
        session = extractSession(info)
        dbRecords = session.query(UserModel).filter_by(id=parent.id).first()
        result = filter(lambda item: item.grouptype_id==type_id, dbRecords.groups)
        return result

    # def resolve_groups(parent, info):
    #     session = extractSession(info)
    #     try:
    #         result = (
    #             session.query(GroupModel)
    #             .join(UserGroupModel, GroupModel.id==UserGroupModel.group_id)
    #             .filter(UserGroupModel.user_id==parent.id)
    #             .all()
    #         )
    #         print(result)
    #     except Exception as e:
    #         print('Error', e)
    #     return result

    events = List('graphqltypes.Event.EventType')
    def resolve_events(parent, info):
        session = extractSession(info)
        try:
            dbRecord = session.query(UserModel).get(parent.id)
        except Exception as e:
            print(e)
        print(f'got dbRecord {dbRecord}')
        #return f'{dir(dbRecord)}'
        try:
            result = dbRecord.events
            print(result)
        except Exception as e:
            print(e)
        return result

    # class CreateUser(Mutation):
    #     class Arguments:
    #         id = ID(required=False)
    #         surname = String(required=False)
    #         name = String(required=False)
    #         email = String(required=False)

    #     ok = Boolean()
    #     user = Field(User)

    #     def mutate(root, info, id=None, name=None, surname=None, email=None):
    #         session = extractSession(info)
    #         dataRecord = UserModel(name=name, surname=surname, email=email)
    #         session.add(dataRecord)
    #         session.commit()
    #         return CreateUser(user=dataRecord, ok=True)

    # class UpdateUser(Mutation):
    #     class Arguments:
    #         id = ID(required=False)
    #         surname = String(required=False)
    #         name = String(required=False)
    #         email = String(required=False)

    #     ok = Boolean()
    #     user = Field(User)

    #     def mutate(root, info, id=None, name=None, surname=None, email=None):
    #         session = extractSession(info)

    #         dataRecord = session.query(UserModel).get(id)
    #         if not(name is None):
    #             dataRecord.name = name
    #         if not(surname is None):
    #             dataRecord.surname = surname
    #         if not(email is None):
    #             dataRecord.email = email
    #         session.commit()

    #         return CreateUser(user=dataRecord, ok=True)