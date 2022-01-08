import re
import sqlalchemy

grapheneMapper = {
    'sqlalchemy.sql.sqltypes.VARCHAR': 'graphene.String',
    'sqlalchemy.dialects.postgresql.base.TIMESTAMP': 'graphene.DateTime',
    'sqlalchemy.sql.sqltypes.BIGINT': 'graphene.Int'
}

def analyseSQLAlchemyBase(SQLAlchemyBase, grapheneMapper=grapheneMapper):
    result = {}
    def analyseSQLAlchemyModel(SQLAlchemyModel):
        inspection = sqlalchemy.inspect(SQLAlchemyModel) 

        result = {
            'SQLTableName' : 'SQLTableName',
            'locals': {},
            'relations': {}
        }
        resolvers = []
        
        #tables = inspection.tables
        #className = f'{tables[0]}'
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
                columnMappedTypeName = grapheneMapper.get(columnMappedTypeName, columnMappedTypeName)
                itemResult['name'] = column.name
                itemResult['type'] = columnMappedTypeName
                if len(columns) > 1:
                    itemResult['unexpected'] = f'there are more columns on {item}'
                result['locals'][itemResult['name']] = itemResult
        for primary_key in inspection.primary_key:
            result['locals'][primary_key.name]['isPrimaryKey'] = True
        #print(inspection.primary_key[0].name)
                
        for item in inspection.relationships.items():
            item1 = item[1]
            if isinstance(item1, sqlalchemy.orm.RelationshipProperty):
                itemResult = {'name': '', 'useList': False, 'type': ''}
                
                referencedTypeName = item1.mapper.class_.__name__
                #referencedTypeNameS = referencedTypeName if referencedTypeName.endswith('s') else referencedTypeName + 's'
                #referencedTypeName = referencedTypeName[:-1] if referencedTypeName.endswith('s') else referencedTypeName
                itemResult['useList'] = item1.uselist
                if item1.uselist:
                    itemResult['name'] = item[0]# referencedTypeNameS
                    itemResult['type'] = referencedTypeName
                else:
                    itemResult['name'] = item[0]# referencedTypeName
                    itemResult['type'] = referencedTypeName

                result['relations'][itemResult['name']] = itemResult
        return result
            
    baseClasses = SQLAlchemyBase.classes
    for item in dir(baseClasses):
        if item.startswith('_'):
            continue
        else:
            itemName = f'{item}'
            result[itemName] = analyseSQLAlchemyModel(getattr(baseClasses, item))
    return result



from jinja2 import Environment, DictLoader, select_autoescape
def renderTemplate(templateName, templatesDict, **variables):
    env = Environment(loader=DictLoader(templatesDict), autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template(templateName)
    return template.render(**variables)

def getSourceCodeForQueryLargeJ2(tableName, dbDescriptor):
    def getObjectItems(tableName):
        tableDescriptor = dbDescriptor[tableName]
        result = []
        for name, item in tableDescriptor['locals'].items():
            result.append(name)# + '\n')
        return result#''.join(result)
    
    tableDescriptor = dbDescriptor[tableName]
    pkName = 'id'
    for name, item in tableDescriptor['locals'].items():
        if item['isPrimaryKey']:
            pkName = name
            break
            
    template = """
/*
 * @param {{pkName}} holds value for unique entity identification
 * @return Future with response from gQL server
 */
export const Query{{tableName}}By{{pkName}}Large = ({{pkName}}) => 
    fetch(rootGQL, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({"query": 
            `
            query {
                {{tableName}}({{pkName}}: ${id}) {
{% for name, item in tableDescriptor['locals'].items() %}
                    {{name}}
{%- endfor %}
{% for name, item in tableDescriptor['relations'].items() %}
                    {{name}} {
    {% for obj in getObjectItems(item['type']) %}
                        {{ obj }}
    {%- endfor %}
                    }
{%- endfor %}
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    
"""
    
    return renderTemplate('template', {'template': template}, tableName=tableName, tableDescriptor=tableDescriptor, pkName=pkName, getObjectItems=getObjectItems)


def getSourceCodeForQueryMediumJ2(tableName, dbDescriptor):
    tableDescriptor = dbDescriptor[tableName]
    pkName = 'id'
    for name, item in tableDescriptor['locals'].items():
        if item['isPrimaryKey']:
            pkName = name
            break
            
    template = """
/*
 * @param {{pkName}} holds value for unique entity identification
 * @return Future with response from gQL server
 */
export const Query{{tableName}}By{{pkName}}Medium = ({{pkName}}) => 
    fetch(rootGQL, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({"query": 
            `
            query {
                {{tableName}}({{pkName}}: ${id}) {
{% for name, item in tableDescriptor['locals'].items() %}
                    {{name}}
{% endfor %}
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    
"""
    return renderTemplate('template', {'template': template}, tableName=tableName, tableDescriptor=tableDescriptor, pkName=pkName)

def getSourceCodeForPageComponentJ2(tableName, dbDescriptor):
    def getObjectItems(tableName):
        tableDescriptor = dbDescriptor[tableName]
        result = []
        for name, item in tableDescriptor['locals'].items():
            result.append(name)# + '\n')
        return result#''.join(result)
    
    tableDescriptor = dbDescriptor[tableName]
    pkName = 'id'
    for name, item in tableDescriptor['locals'].items():
        if item['isPrimaryKey']:
            pkName = name
            break
            
    template = """
export const {{tableName}}Large = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>Title of {{tableName}}</Card.Title>
                    </Card.Header>
                    <Card.Body>
                        <ul class="list-group">
{% for name, item in tableDescriptor['locals'].items() %}
                          <li class="list-group-item">{{name}} : props.{{name}}</li>
{% endfor %}
                        </ul>
                    </Card.Body>
                </Card>
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const {{tableName}}LargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, Query{{tableName}}By{{pkName}}Large, (response) => response.data.{{tableName}}, [props.id])

    if (state !== null) {
        return <{{tableName}}Large {...state} />
    } else if (error !== null) {
        return <LoadingError error={error} />
    } else {
        return <Loading>{props.id}</Loading>
    }
}
    
/*
 * @param props holds extra properties
 * @return 
 */
export const {{tableName}}Page = (props) => {
    const { id } = useParams();

    return (
        <{{tableName}}LargeFetching {...props} id={id} />
    )    

}  
"""
    
    return renderTemplate('template', {'template': template}, tableName=tableName, tableDescriptor=tableDescriptor, pkName=pkName, getObjectItems=getObjectItems)


def getSourceCodeForUpdateMutationJ2(tableName, dbDescriptor):
    tableDescriptor = dbDescriptor[tableName]
    pkName = 'id'
    for name, item in tableDescriptor['locals'].items():
        if item['isPrimaryKey']:
            pkName = name
            break
            
    template = """
class update_{{tableName}}(graphene.Mutation):
    class Arguments:
    {% for name, item in tableDescriptor['locals'].items() %}
        {% if item['isPrimaryKey']: %}
        {{name}} = {{item['type']}}(required=True)
        {% else %}    
        {{name}} = {{item['type']}}(required=False)
        {% endif %}
    {% endfor %}
    ok = graphene.Boolean()
    result = graphene.Field('{{tableName}}')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        dbRecord = session.query({{tableName}}).filter_by({{pkName}}=paramList['{{pkName}}']).one()
        for key, item in paramList.items():
            if key=='{{pkName}}':
                continue
            setattr(dbRecord, key, item)
        session.commit(result)
        return update_{{tableName}}(ok=True, result=dbRecord)
    pass

"""
    return renderTemplate('template', {'template': template}, tableName=tableName, tableDescriptor=tableDescriptor, pkName=pkName)

def getSourceCodeForCreateMutationJ2(tableName, dbDescriptor):
    tableDescriptor = dbDescriptor[tableName]
    template = """
class create_{{tableName}}(graphene.Mutation):
    class Arguments:
    {% for name, item in tableDescriptor['locals'].items() %}
        {{name}} = {{item['type']}}(required=True)
    {% endfor %}
    ok = graphene.Boolean()
    result = graphene.Field('{{tableName}}')
    
    def mutate(parent, info, **paramList):
        session = extractSession(info)
        result = {{tableName}}(**paramList)
        session.add(result)
        session.commit(result)
        return create_{{tableName}}(ok=True, result=result)
    pass

"""
    return renderTemplate('template', {'template': template}, tableName=tableName, tableDescriptor=tableDescriptor)

def getSourceCodeForQueryJ2(tableName, dbDescriptor):
    tableDescriptor = dbDescriptor[tableName]
    template = """
class {{tableName}}(graphene.ObjectType):
    {% for name, item in tableDescriptor['locals'].items() %}
    {{name}} = {{item["type"]}}()
    {% endfor %}
    {% for name, item in tableDescriptor['relations'].items() %}
        {% if item['useList'] %}
    {{name}} = List('{{item["type"]}}')
        {% else %}
    {{name}} = Field('{{item["type"]}}')
        {% endif %}
    def resolver_{{name}}(parent, info):
        return parent.{{name}}
    {% endfor %}
    """
    return renderTemplate('template', {'template': template}, tableName=tableName, tableDescriptor=tableDescriptor)


def getSourceCodeForModelEx(tableName, dbDescriptor):
    tableDescriptor = dbDescriptor[tableName]
    pkName = 'id'
    for name, item in tableDescriptor['locals'].items():
        if item['isPrimaryKey']:
            pkName = name
            break
            
    template = """
class {{tableName}}(BaseModel):
    __tablename__ = '{{tableDescriptor['SQLTableName']}}'
    __table_args__ = {'extend_existing': True} 
    {% for name, item in tableDescriptor['relations'].items() %}
    {{name}} = relationship('{{item['type']}}')#(required=True)
    # {{name}} = association_proxy('{{name}}', 'keyword')
    {% endfor %}
    

"""
    return renderTemplate('template', {'template': template}, tableName=tableName, tableDescriptor=tableDescriptor, pkName=pkName)

import os.path

def generateJS(SQLAlchemyBase, destinationDir='/output/js/'):
    dbDescriptor = analyseSQLAlchemyBase(SQLAlchemyBase)
    for tableName, tableDescription in dbDescriptor.items():
        linesA = getSourceCodeForQueryLargeJ2(tableName, dbDescriptor)
        linesB = getSourceCodeForQueryMediumJ2(tableName, dbDescriptor)
        linesC = getSourceCodeForPageComponentJ2(tableName, dbDescriptor)
        for index in range(99):
            if index == 0:
                fileName = f'{destinationDir}{tableName}.js' 
            else:
                fileName = f'{destinationDir}{tableName}.v{index}.js' 
            
            if os.path.isfile(fileName):
                continue
            
            break

        with open(fileName, 'w') as f:
            f.writelines([linesA, linesB, linesC])
    pass

def generatePythonGQL(SQLAlchemyBase, destinationDir='/output/gql/'):
    dbDescriptor = analyseSQLAlchemyBase(SQLAlchemyBase)
    for tableName, tableDescription in dbDescriptor.items():
        lines = """
import graphene

"""
        linesModel = getSourceCodeForModelEx(tableName, dbDescriptor)
        linesA = getSourceCodeForUpdateMutationJ2(tableName, dbDescriptor)
        linesB = getSourceCodeForCreateMutationJ2(tableName, dbDescriptor)
        linesC = getSourceCodeForQueryJ2(tableName, dbDescriptor)
        for index in range(99):
            if index == 0:
                fileName = f'{destinationDir}{tableName}.py' 
            else:
                fileName = f'{destinationDir}{tableName}.v{index}.py' 
            
            if os.path.isfile(fileName):
                continue
            
            break

        with open(fileName, 'w') as f:
            f.writelines([lines, linesModel, linesA, linesB, linesC])
    pass




def generatePythonModelEx(SQLAlchemyBase, destinationDir='/output/'):
    
    imports = """
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

from sqlalchemy import Column, String, BigInteger, DateTime, TIMESTAMP
from sqlalchemy import Table, ForeignKey, Sequence, text, relationship
from sqlalchemy.sql import func
    """
    resultLines = [imports]

    dbDescriptor = analyseSQLAlchemyBase(SQLAlchemyBase)
    for tableName, tableDescription in dbDescriptor.items():
        lines = getSourceCodeForModelEx(tableName, dbDescriptor)
        resultLines.append(lines)
        pass
    
    with open(f'{destinationDir}modelEx.py', 'w') as f:
        f.writelines(resultLines)

    return resultLines

import jinja2


def generatePythonGQLFull(SQLAlchemyBase, destinationDir='/output/gql/'):
    dbDescriptor = analyseSQLAlchemyBase(SQLAlchemyBase)

    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "gql.main.py.template"
    template = templateEnv.get_template(TEMPLATE_FILE)

    for index in range(99):
        if index == 0:
            fileName = f'{destinationDir}gql_app.py' 
        else:
            fileName = f'{destinationDir}gql_app.v{index}.py' 
        
        if os.path.isfile(fileName):
            continue
        
        break

    outputText = template.render(dbDescriptor=dbDescriptor)  # this is where to put args to the template renderer
    with open(fileName, 'w') as f:
        f.writelines([outputText])


    TEMPLATE_FILE = "gql.py.template"
    template = templateEnv.get_template(TEMPLATE_FILE)

    for tableName, tableDescriptor in dbDescriptor.items():

        pkName = 'id'
        for name, item in tableDescriptor['locals'].items():
            if item['isPrimaryKey']:
                pkName = name
                break

        outputText = template.render(tableName=tableName, tableDescriptor=tableDescriptor, pkName=pkName)  # this is where to put args to the template renderer

        for index in range(99):
            if index == 0:
                fileName = f'{destinationDir}gql_{tableName}.py' 
            else:
                fileName = f'{destinationDir}gql_{tableName}.v{index}.py' 
            
            if os.path.isfile(fileName):
                continue
            
            break


        with open(fileName, 'w') as f:
            f.writelines([outputText])

    return outputText


def generateJSGQLFull(SQLAlchemyBase, destinationDir='/output/js/'):
    def getObjectItems(tableName):
        tableDescriptor = dbDescriptor[tableName]
        result = []
        for name, item in tableDescriptor['locals'].items():
            result.append(name)# + '\n')
        return result#''.join(result)

    dbDescriptor = analyseSQLAlchemyBase(SQLAlchemyBase)

    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "gql.js.template"
    template = templateEnv.get_template(TEMPLATE_FILE)

    for tableName, tableDescriptor in dbDescriptor.items():

        pkName = 'id'
        for name, item in tableDescriptor['locals'].items():
            if item['isPrimaryKey']:
                pkName = name
                break

        outputText = template.render(tableName=tableName, tableDescriptor=tableDescriptor, pkName=pkName, getObjectItems=getObjectItems)  # this is where to put args to the template renderer

        for index in range(99):
            if index == 0:
                fileName = f'{destinationDir}{tableName}.js' 
            else:
                fileName = f'{destinationDir}{tableName}.v{index}.js' 
            
            if os.path.isfile(fileName):
                continue
            break

        with open(fileName, 'w') as f:
            f.writelines([outputText])

    return outputText

def createFilter(name, filterDescription):
    
    def createBetween(low, high):
        def between(item):
            value = item[name]
            return (value >= low) & (value <= high)
        return between
    return bounds
