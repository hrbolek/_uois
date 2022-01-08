import {
    Link,
    useParams
  } from "react-router-dom";
import { useEffect, useState } from "react";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';

import { useQueryGQL, LoadingError, Loading } from './utils';
import { root } from './setup';

/*
 * @param id holds value for unique entity identification
 * @return Future with response from gQL server
 */
export const QueryGroupModelByidLarge = (id) => 
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
                GroupModel(id: ${id}) {

                    id
                    name
                    abbreviation
                    lastchange
                    entryYearId
                    externalId
                    UIC
                    grouptype_id

                    grouptypemodel {
    
                        id
                        name
                    }
                    groupconnectionmodel_collection {
    
                        id
                        child_id
                        parent_id
                    }
                    usergroupmodel_collection {
    
                        id
                        user_id
                        group_id
                    }
                    rolemodel_collection {
    
                        id
                        name
                        lastchange
                        roletype_id
                        user_id
                        group_id
                    }
                    eventgroupmodel_collection {
    
                        id
                        group_id
                        event_id
                    }
                    studyplangroupsmodel_collection {
    
                        id
                        studyplan_id
                        group_id
                    }
                    studyplanitemgroupmodel_collection {
    
                        id
                        group_id
                        studyplanitem_id
                    }
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

/*
 * @param id holds value for unique entity identification
 * @return Future with response from gQL server
 */
export const QueryGroupModelByidMedium = (id) => 
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
                GroupModel(id: ${id}) {
                    id
                    name
                    abbreviation
                    lastchange
                    entryYearId
                    externalId
                    UIC
                    grouptype_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/GroupModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const GroupModelSmall = (props) =>  {
    if (props.name) {
        return (
            <Link to={entityRoot + `/${props.id}`}>{props.name}{props.children}</Link>
        )
    } else if (props.label) {
        return (
            <Link to={entityRoot + `/${props.id}`}>{props.label}{props.children}</Link>
        )
    } else {
        return (
            <Link to={entityRoot + `/${props.id}`}>{props.id}{props.children}</Link>
        )
    } 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const GroupModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of GroupModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">abbreviation : { props.abbreviation }</li>
                    <li class="list-group-item">lastchange : { props.lastchange }</li>
                    <li class="list-group-item">entryYearId : { props.entryYearId }</li>
                    <li class="list-group-item">externalId : { props.externalId }</li>
                    <li class="list-group-item">UIC : { props.UIC }</li>
                    <li class="list-group-item">grouptype_id : { props.grouptype_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @param props.abbreviation
 * @param props.lastchange
 * @param props.entryYearId
 * @param props.externalId
 * @param props.UIC
 * @param props.grouptype_id
 * @return 
 */
export const GroupModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
            <td>{ props.abbreviation }</td>
            <td>{ props.lastchange }</td>
            <td>{ props.entryYearId }</td>
            <td>{ props.externalId }</td>
            <td>{ props.UIC }</td>
            <td>{ props.grouptype_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const GroupModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>name</th>
            <th>abbreviation</th>
            <th>lastchange</th>
            <th>entryYearId</th>
            <th>externalId</th>
            <th>UIC</th>
            <th>grouptype_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of GroupModel
 * @return 
 */
export const GroupModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <GroupModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <GroupModelTableHeadRow />
            </thead>
            <tbody>
                {rows}
            </tbody>
        </Table>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const GroupModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <GroupModelMedium {...props}> 
                </GroupModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const GroupModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryGroupModelByidLarge, (response) => response.data.GroupModel, [props.id])

    if (state !== null) {
        return <GroupModelLarge {...state} />
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
export const GroupModelPage = (props) => {
    const { id } = useParams();

    return (
        <GroupModelLargeFetching {...props} id={id} />
    )    

}  