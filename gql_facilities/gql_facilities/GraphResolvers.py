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

from gql_facilities.DBDefinitions import BaseModel

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

from gql_facilities.DBDefinitions import FacilityTypeModel, FacilityModel, EventFacilityModel, EventFacilityStateType

###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

resolveFacilityById = createEntityByIdGetter(FacilityModel)
resolveFacilityPage = createEntityGetter(FacilityModel)
resolveFacilitiesByGroup = create1NGetter(FacilityModel, foreignKeyName="group_id")
resolveFacilitiesByFacility = create1NGetter(
    FacilityModel, foreignKeyName="master_facility_id"
)

resolveFacityTypeById = createEntityByIdGetter(FacilityTypeModel)

facilityPageStatement = select(FacilityModel)
facilityTypePageStatement = select(FacilityTypeModel)
facilityStateTypePageStatement = select(EventFacilityStateType)