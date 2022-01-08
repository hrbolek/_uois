from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

from sqlalchemy_utils.functions import database_exists, create_database
import json

import models

with open('config.json', 'r') as f:
    config = json.load(f)

connectionstring = config['connectionstring']

if not database_exists(connectionstring):  #=> False
    try:
        create_database(connectionstring)
        print('Database created')
    except Exception as e:
        print('Database does not exists and cannot be created')
        raise

BaseModel = models.BaseModel
engine = create_engine(connectionstring)
#BaseModel.metadata.drop_all(engine)
#print('DB Drop Done')
#BaseModel.metadata.create_all(engine)
#print('DB Create All Done')

print('DONE')

import sqlalchemy

def analyseSQLAlchemyBase(SQLAlchemyBase):
    result = {}
    def analyseSQLAlchemyModel(SQLAlchemyModel):
        inspection = sqlalchemy.inspect(SQLAlchemyModel) 

        result = {
            'SQLTableName' : 'SQLTableName',
            'locals': {},
            'relations': {}
        }
        result['SQLTableName'] = f'{inspection.tables[0]}'

        for item in inspection.iterate_properties:
            if hasattr(item, 'columns'):
                
                itemResult = {'name': '', 'type': '', 'column': None, 'isPrimaryKey': False}
                columns = item.columns
                column = columns[0]
                #print(dir(column))
                itemResult['column'] = column.name
                columnType = column.type
                columnMappedTypeName = f'{columnType.__module__}.{type(columnType).__qualname__}'
                itemResult['name'] = column.name
                itemResult['type'] = columnMappedTypeName
                if len(columns) > 1:
                    itemResult['unexpected'] = f'there are more columns on {item}'
                result['locals'][itemResult['name']] = itemResult
        for primary_key in inspection.primary_key:
            result['locals'][primary_key.name]['isPrimaryKey'] = True
                
        for item in inspection.relationships.items():
            item1 = item[1]
            if isinstance(item1, sqlalchemy.orm.RelationshipProperty):
                itemResult = {'name': '', 'useList': False, 'type': ''}
                
                referencedTypeName = item1.mapper.class_.__name__
                itemResult['useList'] = item1.uselist
                if item1.uselist:
                    itemResult['name'] = item[0]# referencedTypeNameS
                    itemResult['type'] = referencedTypeName
                else:
                    itemResult['name'] = item[0]# referencedTypeName
                    itemResult['type'] = referencedTypeName

                result['relations'][itemResult['name']] = itemResult
        return result
            
    for item in SQLAlchemyBase.registry.mappers:
        #result[f'{item.__name__}'] = analyseSQLAlchemyModel(item)
        result[f'{item.tables[0].name}'] = {'Model': f'{item.class_.__name__}', **analyseSQLAlchemyModel(item)}
    return result


print(analyseSQLAlchemyBase(BaseModel))