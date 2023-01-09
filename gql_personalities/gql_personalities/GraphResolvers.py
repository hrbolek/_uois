
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_personalities.DBDefinitions import BaseModel, UserModel, Rank, Study, Certificate, Medal, WorkHistory, RelatedDoc
from gql_personalities.DBDefinitions import RankType, CertificateType, MedalType
from gql_personalities.DBDefinitions import CertificateTypeGroup, MedalTypeGroup

#user resolvers
resolveUserById = createEntityByIdGetter(UserModel)
resolveUserAll = createEntityGetter(UserModel)

resolveRanksForUser = create1NGetter(Rank, foreignKeyName='user_id', options=joinedload(Rank.rankType))
resolveStudiesForUser = create1NGetter(Study, foreignKeyName='user_id')
resolveCertificatesForUser = create1NGetter(Certificate, foreignKeyName='user_id', options=joinedload(Certificate.certificateType))
resolveMedalsForUser = create1NGetter(Medal, foreignKeyName='user_id', options=joinedload(Medal.medalType))
resolveWorkHistoriesForUser = create1NGetter(WorkHistory, foreignKeyName='user_id')
resolveRelatedDocsForUser = create1NGetter(RelatedDoc, foreignKeyName='user_id')

#rank resolvers
resolveRankById = createEntityByIdGetter(Rank)
resolveRankAll = createEntityGetter(Rank)
resolverUpdateRank = createUpdateResolver(Rank)
resolveInsertRank = createInsertResolver(Rank)

#rankType resolvers
resolveRankTypeById = createEntityByIdGetter(RankType)
resolveRankTypeAll = createEntityGetter(RankType)
resolverUpdateRankType = createUpdateResolver(RankType)
resolveInsertRankType = createInsertResolver(RankType)

async def resolveRankTypeByThreeLetters(session: AsyncSession, validity = None, letters: str = '') -> List[Rank]:
    if len(letters) < 3:
        return []
    stmt = select(RankType).where(RankType.name.like(f'%{letters}%'))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


#study resolvers
resolveStudyById = createEntityByIdGetter(Study)
resolveStudyAll = createEntityGetter(Study)
resolverUpdateStudy = createUpdateResolver(Study)
resolveInsertStudy = createInsertResolver(Study)

async def resolveStudyByThreeLetters(session: AsyncSession, validity = None, letters: str = '') -> List[Study]:
    if len(letters) < 3:
        return []
    stmt = select(Study).where(Study.place.like(f'%{letters}%'))  #Study.place. ... kvůli názvu v entitě
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


#certificate resolvers
resolveCertificateById = createEntityByIdGetter(Certificate)
resolveCertificateAll = createEntityGetter(Certificate)
resolverUpdateCertificate = createUpdateResolver(Certificate)
resolveInsertCertificate = createInsertResolver(Certificate)


#certificateType resolvers
resolveCertificateTypeById = createEntityByIdGetter(CertificateType)
resolveCertificateTypeAll = createEntityGetter(CertificateType)
resolverUpdateCertificateType = createUpdateResolver(CertificateType)
resolveInsertCertificateType = createInsertResolver(CertificateType)

async def resolveCertificateTypeByThreeLetters(session: AsyncSession, validity = None, letters: str = '') -> List[CertificateType]:
    if len(letters) < 3:
        return []
    stmt = select(CertificateType).where(CertificateType.name.like(f'%{letters}%'))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


#certificateTypeGroup resolvers
resolveCertificateTypeGroupById = createEntityByIdGetter(CertificateTypeGroup)
resolveCertificateTypeGroupAll = createEntityGetter(CertificateTypeGroup)
resolverUpdateCertificateTypeGroup = createUpdateResolver(CertificateTypeGroup)
resolveInsertCertificateTypeGroup = createInsertResolver(CertificateTypeGroup)

async def resolveCertificateTypeGroupByThreeLetters(session: AsyncSession, validity = None, letters: str = '') -> List[CertificateTypeGroup]:
    if len(letters) < 3:
        return []
    stmt = select(CertificateTypeGroup).where(CertificateTypeGroup.name.like(f'%{letters}%'))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


#medal resolvers
resolveMedalById = createEntityByIdGetter(Medal)
resolveMedalAll = createEntityGetter(Medal)
resolverUpdateMedal = createUpdateResolver(Medal)
resolveInsertMedal = createInsertResolver(Medal)


#medalType resolvers
resolveMedalTypeById = createEntityByIdGetter(MedalType)
resolveMedalTypeAll = createEntityGetter(MedalType)
resolverUpdateMedalType = createUpdateResolver(MedalType)
resolveInsertMedalType = createInsertResolver(MedalType)

async def resolveMedalTypeByThreeLetters(session: AsyncSession, validity = None, letters: str = '') -> List[MedalType]:
    if len(letters) < 3:
        return []
    stmt = select(MedalType).where(MedalType.name.like(f'%{letters}%'))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


#medalTypeGroup resolvers
resolveMedalTypeGroupById = createEntityByIdGetter(MedalTypeGroup)
resolveMedalTypeGroupAll = createEntityGetter(MedalTypeGroup)
resolverUpdateMedalTypeGroup = createUpdateResolver(MedalTypeGroup)
resolveInsertMedalTypeGroup = createInsertResolver(MedalTypeGroup)

async def resolveMedalTypeGroupByThreeLetters(session: AsyncSession, validity = None, letters: str = '') -> List[MedalTypeGroup]:
    if len(letters) < 3:
        return []
    stmt = select(MedalTypeGroup).where(MedalTypeGroup.name.like(f'%{letters}%'))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


#workHistory resolvers
resolveWorkHistoryById = createEntityByIdGetter(WorkHistory)
resolveWorkHistoryAll = createEntityGetter(WorkHistory)
resolverUpdateWorkHistory = createUpdateResolver(WorkHistory)
resolveInsertWorkHistory = createInsertResolver(WorkHistory)

async def resolveWorkHistoryByThreeLetters(session: AsyncSession, validity = None, letters: str = '') -> List[WorkHistory]:
    if len(letters) < 3:
        return []
    stmt = select(WorkHistory).where(WorkHistory.name.like(f'%{letters}%'))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()


#relatedDoc resolvers
resolveRelatedDocById = createEntityByIdGetter(RelatedDoc)
resolveRelatedDocAll = createEntityGetter(RelatedDoc)
resolverUpdateRelatedDoc = createUpdateResolver(RelatedDoc)
resolveInsertRelatedDoc = createInsertResolver(RelatedDoc)

async def resolveRelatecDocByThreeLetters(session: AsyncSession, validity = None, letters: str = '') -> List[RelatedDoc]:
    if len(letters) < 3:
        return []
    stmt = select(RelatedDoc).where(RelatedDoc.name.like(f'%{letters}%'))
    if validity is not None:
        stmt = stmt.filter_by(valid=True)

    dbSet = await session.execute(stmt)
    return dbSet.scalars()

###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

