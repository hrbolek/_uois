from sqlalchemy.ext.declarative import declarative_base

from functools import cache

@cache
def getBaseModel():
    """creates and cache a BaseModel
    
    Returns
    -------
    BaseModel
        it is instance of declarative_base from SQLAlchemy
    """
    BaseModel = declarative_base()
    print('BaseModel cached')
    return BaseModel


BaseModel = getBaseModel()