from sqlalchemy.ext.declarative import declarative_base

from functools import cache

@cache
def getBaseModel():
    BaseModel = declarative_base()
    print('BaseModel cached')
    return BaseModel