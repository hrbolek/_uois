import {
    Link,
    useParams
  } from "react-router-dom";
import { useEffect, useState } from "react";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';

import { useQueryGQL, LoadingError, Loading } from '../index';
import { root, rootGQL } from '../setup';

/*
 * @param id holds value for unique entity identification
 * @return Future with response from gQL server
 */
export const QueryBuildingModelByidLarge = (id) => 
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
                buildingsById(id: ${id}) {

                    id
                    name
                    lastchange
                    externalId
                    areal_id

                    arealmodel {
    
                        id
                        name
                        externalId
                        lastchange
                    }
                    roommodels {
    
                        id
                        name
                        lastchange
                        externalId
                        building_id
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
export const QueryBuildingModelByidMedium = (id) => 
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
                buildingsById(id: ${id}) {
                    id
                    name
                    lastchange
                    externalId
                    areal_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/buildings';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const BuildingModelSmall = (props) =>  {
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
export const BuildingModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of BuildingModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">lastchange : { props.lastchange }</li>
                    <li class="list-group-item">externalId : { props.externalId }</li>
                    <li class="list-group-item">areal_id : { props.areal_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @param props.lastchange
 * @param props.externalId
 * @param props.areal_id
 * @return 
 */
export const BuildingModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
            <td>{ props.lastchange }</td>
            <td>{ props.externalId }</td>
            <td>{ props.areal_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const BuildingModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th><BuildingModelSmall {...props} /></th>
            <th>name</th>
            <th>lastchange</th>
            <th>externalId</th>
            <th>areal_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of BuildingModel
 * @return 
 */
export const BuildingModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <BuildingModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <BuildingModelTableHeadRow />
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
export const BuildingModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <BuildingModelMedium {...props}> 
                </BuildingModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const BuildingModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryBuildingModelByidLarge, (response) => response.data.BuildingModel, [props.id])

    if (state !== null) {
        return <BuildingModelLarge {...state} />
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
export const BuildingModelPage = (props) => {
    const { id } = useParams();

    return (
        <BuildingModelLargeFetching {...props} id={id} />
    )    

}  