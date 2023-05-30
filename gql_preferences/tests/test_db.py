#preferedtagentities
import pytest
from sqlalchemy import select
from .creators import createDBTest
from .shared import (
    prepare_in_memory_sqllite,
    prepare_demodata,
    get_demodata
)

from gql_preferences.DBDefinitions import (
    TagEntityModel, TagModel
)

test_TagEntityModel = createDBTest("preferedtagentities", TagEntityModel)
test_TagModel = createDBTest("preferedtags", TagModel)

@pytest.mark.asyncio
async def test_TagModelDB():
    tableName = "preferedtags"
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)

    data = get_demodata()
    table = data[tableName]

    print(table, flush=True)
    for row in table:
        print(row, flush=True)
        async with  async_session_maker() as session:
            rowid = row['author_id']
            stmt = select(TagModel).filter_by(author_id=rowid)
            result = await session.execute(stmt)
            row = result.scalar()
            # row = select(dbModel).filter_by(id=rowid).execute(session)
            
        assert row is not None

    
