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
export const QueryGroupConnectionModelByidLarge = (id) => 
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
                GroupConnectionModel(id: ${id}) {

                    id
                    child_id
                    parent_id

                    groupmodel {
    
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
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

/*
 * @param id holds value for unique entity identification
 * @return Future with response from gQL server
 */
export const QueryGroupConnectionModelByidMedium = (id) => 
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
                GroupConnectionModel(id: ${id}) {
                    id
                    child_id
                    parent_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/GroupConnectionModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const GroupConnectionModelSmall = (props) =>  {
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
export const GroupConnectionModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of GroupConnectionModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">child_id : { props.child_id }</li>
                    <li class="list-group-item">parent_id : { props.parent_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.child_id
 * @param props.parent_id
 * @return 
 */
export const GroupConnectionModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.child_id }</td>
            <td>{ props.parent_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const GroupConnectionModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>child_id</th>
            <th>parent_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of GroupConnectionModel
 * @return 
 */
export const GroupConnectionModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <GroupConnectionModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <GroupConnectionModelTableHeadRow />
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
export const GroupConnectionModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <GroupConnectionModelMedium {...props}> 
                </GroupConnectionModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const GroupConnectionModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryGroupConnectionModelByidLarge, (response) => response.data.GroupConnectionModel, [props.id])

    if (state !== null) {
        return <GroupConnectionModelLarge {...state} />
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
export const GroupConnectionModelPage = (props) => {
    const { id } = useParams();

    return (
        <GroupConnectionModelLargeFetching {...props} id={id} />
    )    

}  