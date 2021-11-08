from fastapi import FastAPI, Request

import models.BaseEntities as BEntities
import models.BaseEntityTypes as BETypes
import models.Relations as Relations

import sqlengine.sqlengine as SqlEngine
from sqlalchemy import Sequence

connectionString = 'postgresql+psycopg2://postgres:example@postgres/jupyterII'

UserModel, GroupModel, ClassRoomModel, EventModel = BEntities.GetModels()
GroupTypeModel, RoleTypesModel = BETypes.GetModels()
Relations.createRelations()

Session = SqlEngine.init(connectionString)

#from contextlib import contextmanager
#@contextmanager
#def session_scope():
#    """Provide a transactional scope around a series of operations."""
#    session = Session()
#    try:
#        yield session
#        session.commit()
#    except:
#        session.rollback()
#        raise
#    finally:
#        session.close()

async def prepareSession():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()    


from fastapi import Depends
def attachFastApi(app):

    apiapp = FastAPI()

    @apiapp.get("/items/{item_id}")
    async def apif_read_item(item_id: int):
        
        return {"item_id": item_id}

    @apiapp.get("/")
    async def apif_root():
        return {"message": "Hello World"}


    @apiapp.get("/users/{id}")
    async def users_get_by_id(id: int, session=Depends(prepareSession)):
        result = session.query(UserModel).get(id)
        return result

    @apiapp.get("/users/")
    async def users_get_all(skip: int = 0, limit: int = 10, session=Depends(prepareSession)):
        result = []
        result = session.query(UserModel).offset(skip).limit(limit).all()
        return result

    @apiapp.get("/users/{id}")
    async def users_get_by_id(id: int, session=Depends(prepareSession)):
        result = session.query(UserModel).get(id)
        return result

    @apiapp.get("/groups/")
    async def groups_get_all(skip: int = 0, limit: int = 10, session=Depends(prepareSession)):
        result = []
        result = session.query(GroupModel).offset(skip).limit(limit).all()
        return result

    @apiapp.get("/groups/{id}")
    async def groups_get_by_id(id: int, session=Depends(prepareSession)):
        result = session.query(GroupModel).get(id)
        return result

    @apiapp.get("/classrooms/")
    async def classrooms_get_all(skip: int = 0, limit: int = 10, session=Depends(prepareSession)):
        result = []
        result = session.query(ClassRoomModel).offset(skip).limit(limit).all()
        return result

    @apiapp.get("/classrooms/{id}")
    async def classrooms_get_by_id(id: int, session=Depends(prepareSession)):
        result = session.query(ClassRoomModel).get(id)
        return result

    @apiapp.get("/events/")
    async def events_get_all(skip: int = 0, limit: int = 10, session=Depends(prepareSession)):
        result = []
        result = session.query(EventModel).offset(skip).limit(limit).all()
        return result

    @apiapp.get("/events/{id}")
    async def events_get_by_id(id: int, session=Depends(prepareSession)):
        result = session.query(EventModel).get(id)
        return result

    app.mount('/api', apiapp)