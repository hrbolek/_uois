def initModels():
    """Build relations among entities
    """
    print('building all relations')
    from . import BaseEntities
    BaseEntities.BuildRelations()
    from . import FacilityEntities
    FacilityEntities.BuildRelations()
    from . import TimeTableEntities
    TimeTableEntities.BuildRelations()
    print('building all relations finished')
    pass

