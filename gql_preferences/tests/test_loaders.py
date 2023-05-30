#preferedtagentities
import pytest
from sqlalchemy import select
from .shared import (
    prepare_in_memory_sqllite,
    prepare_demodata,
    get_demodata,
    createContext
)

from gql_preferences.DBDefinitions import (
    TagEntityModel, TagModel
)

@pytest.mark.asyncio
async def test_TagModelDB():
    tableName = "preferedtags"
    async_session_maker = await prepare_in_memory_sqllite()
    await prepare_demodata(async_session_maker)
    context = await createContext(async_session_maker)
    loaders = context["all"]
    loader = loaders.tagentities
    stmt = loader.getSelectStatement()
    result = await loader.execute_select(stmt)
    for item in result:
        print(item.id, item.author_id)


    
