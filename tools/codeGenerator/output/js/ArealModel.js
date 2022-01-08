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
export const QueryArealModelByidLarge = (id) => 
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
                ArealModel(id: ${id}) {

                    id
                    name
                    externalId
                    lastchange

                    buildingmodel_collection {
    
                        id
                        name
                        lastchange
                        externalId
                        areal_id
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
export const QueryArealModelByidMedium = (id) => 
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
                ArealModel(id: ${id}) {
                    id
                    name
                    externalId
                    lastchange
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/ArealModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const ArealModelSmall = (props) =>  {
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
export const ArealModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of ArealModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">externalId : { props.externalId }</li>
                    <li class="list-group-item">lastchange : { props.lastchange }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @param props.externalId
 * @param props.lastchange
 * @return 
 */
export const ArealModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
            <td>{ props.externalId }</td>
            <td>{ props.lastchange }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const ArealModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>name</th>
            <th>externalId</th>
            <th>lastchange</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of ArealModel
 * @return 
 */
export const ArealModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <ArealModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <ArealModelTableHeadRow />
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
export const ArealModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <ArealModelMedium {...props}> 
                </ArealModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const ArealModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryArealModelByidLarge, (response) => response.data.ArealModel, [props.id])

    if (state !== null) {
        return <ArealModelLarge {...state} />
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
export const ArealModelPage = (props) => {
    const { id } = useParams();

    return (
        <ArealModelLargeFetching {...props} id={id} />
    )    

}  