from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

from sqlalchemy_schemadisplay import create_schema_graph
import json


with open('tablenames.json', 'r') as f:
    tablenames = json.load(f)

with open('config.json', 'r') as f:
    config = json.load(f)

connectionstring = config['connectionstring']

Base = automap_base()
engine = create_engine(connectionstring)

import copy

tablenamesNew = copy.deepcopy(tablenames)
def fromTableToModelName(base, tablename, table):
    tabledesc = tablenamesNew.get(tablename, None)
    if tabledesc is None:
        result = tablename
        tablenamesNew[tablename] = {'SQLTableName': tablename, 'Model': tablename}
    else:
        result = tabledesc.get('Model', tablename)
        tablenamesNew[tablename]['Model'] = result
    return result

def fromTableToRelationNName(base, local_cls, referred_cls, constraint):
    appendix = "s"
    tablename = local_cls.__name__
    tabledesc = tablenamesNew.get(tablename, None)
    if tabledesc is None:
        result = referred_cls.__name__.lower() + appendix
        tabledesc = {'relations': {referred_cls.__name__: {'name': result}}}
        tablenamesNew[tablename] = tabledesc
    else:
        result = referred_cls.__name__.lower() + appendix
        relations = tabledesc.get('relations', None)
        if relations is None:
            relations = {referred_cls.__name__: {'name': result}}
            tabledesc['relations'] = relations
        else:
            referredTableDesc = relations.get(referred_cls.__name__, None)
            if referredTableDesc is None:
                referredTableDesc = {'name': result}
                relations[referred_cls.__name__] = referredTableDesc
            result = referredTableDesc.get('name', result)
            referredTableDesc['name'] = result
    return result

def fromTableToRelation1Name(base, local_cls, referred_cls, constraint):
    appendix = ""
    tablename = local_cls.__name__
    tabledesc = tablenamesNew.get(tablename, None)
    if tabledesc is None:
        result = referred_cls.__name__.lower() + appendix
        tabledesc = {'relations': {referred_cls.__name__: {'name': result}}}
        tablenamesNew[tablename] = tabledesc
    else:
        result = referred_cls.__name__.lower() + appendix
        relations = tabledesc.get('relations', None)
        if relations is None:
            relations = {referred_cls.__name__: {'name': result}}
            tabledesc['relations'] = relations
        else:
            referredTableDesc = relations.get(referred_cls.__name__, None)
            if referredTableDesc is None:
                referredTableDesc = {'name': result}
                relations[referred_cls.__name__] = referredTableDesc
            result = referredTableDesc.get('name', result)
            referredTableDesc['name'] = result
    return result

print('Extracting metadata ...')
Base.prepare(engine, reflect=True,
    classname_for_table=fromTableToModelName,
    name_for_collection_relationship=fromTableToRelationNName,
    name_for_scalar_relationship=fromTableToRelation1Name
    )

with open('/output/tablenamesnew.json', 'w') as f:
    json.dump(tablenamesNew, f, indent=4)

print('Creating graph for DB Schema ...')
# create the pydot graph object by autoloading all tables via a bound metadata object
graph = create_schema_graph(metadata=MetaData(connectionstring),
    show_datatypes=False, # The image would get nasty big if we'd show the datatypes
    show_indexes=False, # ditto for indexes
    rankdir='LR', # From left to right (instead of top to bottom)
    concentrate=False # Don't try to join the relation lines together
)
print('Writing ...')
graph.write_png('/output/img/dbschema.png') # write out the file
graph.write_png('/output/img/dbschema.svg') # write out the file

print('Creating extended graph for DB Schema ...')
graph = create_schema_graph(metadata=MetaData(connectionstring),
    show_datatypes=True, # The image would get nasty big if we'd show the datatypes
    show_indexes=False, # ditto for indexes
    rankdir='LR', # From left to right (instead of top to bottom)
    concentrate=False # Don't try to join the relation lines together
)
print('Writing ...')
graph.write_png('/output/img/dbschema_ex.png') # write out the file
graph.write_svg('/output/img/dbschema_ex.svg') # write out the file

from sqlalchemy_schemadisplay import create_uml_graph

print('Creating graph for UML ...')
def getModels(SQLAlchemyBase=Base):
    baseClasses = SQLAlchemyBase.classes
    result = []
    for item in dir(baseClasses):
        if item.startswith('_'):
            continue
        result.append(getattr(baseClasses, item))
    return result

mappers = [cls.__mapper__ for cls in getModels(SQLAlchemyBase=Base)]
graph = create_uml_graph(mappers,
    show_operations=False, # not necessary in this case
    show_multiplicity_one=False # some people like to see the ones, some don't
)
print('Writing UML...')
graph.write_png('/output/img/uml.png') # write out the file
graph.write_svg('/output/img/uml.svg') # write out the file

from sourceCodeGenerators import analyseSQLAlchemyBase, generateJS, generatePythonGQL, generatePythonModelEx, generatePythonGQLFull, generateJSGQLFull

print('Analysing DB...')
#analysisResult = analyseSQLAlchemyBase(Base)
print('Generate JS source codes...')
#generateJS(Base)

#print('Generate Python source codes...')
#generatePythonGQL(Base)

#print('Generate Python extended models...')
#generatePythonModelEx(Base)

print('Generate Python GQL files...')
generatePythonGQLFull(Base)

print('Generate JS GQL files...')
generateJSGQLFull(Base)
# from eralchemy import render_er

# ## Draw from database
# render_er(connectionstring, '/output/dbschemaII.png')

print('DONE')