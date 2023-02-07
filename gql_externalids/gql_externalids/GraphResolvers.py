from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import (
    create1NGetter,
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
    createUpdateResolver,
)
from uoishelpers.resolvers import putSingleEntityToDb

from gql_externalids.DBDefinitions import BaseModel

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

from gql_externalids.DBDefinitions import ExternalIdModel, ExternalIdTypeModel


###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

resolveExternalIds = create1NGetter(ExternalIdModel, foreignKeyName="inner_id")
resolveExternalIdById = createEntityByIdGetter(ExternalIdModel)

resolveExternalTypeById = createEntityByIdGetter(ExternalIdTypeModel)
resolveExternalTypePaged = createEntityGetter(ExternalIdTypeModel)


async def resolveExternalIdIntoInnerId(session, externalid, typeid):
    """Resolver transformujici externi id daneho typu na interni id (uuid)"""
    stmt = select(ExternalIdModel).filter(
        ExternalIdModel.typeid_id == typeid, ExternalIdModel.outer_id == externalid
    )
    dbSet = await session.execute(stmt)
    result = next(dbSet.scalars(), None)
    return result


async def resolveInnerIdIntoExternalIds(session, internalid, typeid=None):
    """resolver transformujici interni id na viceprvkovy vektor externich id nebo na jednoprvkovy vektor
    je-li urcen typ externiho id, vraceny vektor muze byt prazdny, pokud nebylo nic nalezeno
    """
    if typeid is None:
        stmt = select(ExternalIdModel).filter(ExternalIdModel.inner_id == internalid)
    else:
        stmt = select(ExternalIdModel).filter(
            ExternalIdModel.typeid_id == typeid, ExternalIdModel.inner_id == internalid
        )

    dbSet = await session.execute(stmt)
    # result = list(map(lambda row: row.outer_id, dbSet.scalars()))
    return dbSet.scalars()


async def resolveAssignExternalId(session, internalid, externalid, typeid):
    """resolver prirazujici externi id daneho typu internimu id
    existuje-li takove prirazeni, je aktualizovano
    jinak je vytvoreno
    """
    stmt = select(ExternalIdModel).filter(
        ExternalIdModel.typeid_id == typeid, ExternalIdModel.inner_id == internalid
    )
    dbSet = await session.execute(stmt)
    dbRecord = next(dbSet.scalars(), None)
    if dbRecord is None:
        dbRecord = ExternalIdModel(
            typeid_id=typeid, inner_id=internalid, outer_id=externalid
        )

        session.add(dbRecord)
        await session.commit()  # session.flush()
    else:
        dbRecord.outer_id = externalid
        await session.commit()
    return dbRecord


# ...
