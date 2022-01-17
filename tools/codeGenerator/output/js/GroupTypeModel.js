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
export const QueryGroupTypeModelByidLarge = (id) => 
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
                grouptypesById(id: ${id}) {

                    id
                    name

                    groupmodels {
    
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
export const QueryGroupTypeModelByidMedium = (id) => 
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
                grouptypesById(id: ${id}) {
                    id
                    name
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/grouptypes';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const GroupTypeModelSmall = (props) =>  {
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
export const GroupTypeModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of GroupTypeModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @return 
 */
export const GroupTypeModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const GroupTypeModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th><GroupTypeModelSmall {...props} /></th>
            <th>name</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of GroupTypeModel
 * @return 
 */
export const GroupTypeModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <GroupTypeModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <GroupTypeModelTableHeadRow />
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
export const GroupTypeModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <GroupTypeModelMedium {...props}> 
                </GroupTypeModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const GroupTypeModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryGroupTypeModelByidLarge, (response) => response.data.GroupTypeModel, [props.id])

    if (state !== null) {
        return <GroupTypeModelLarge {...state} />
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
export const GroupTypeModelPage = (props) => {
    const { id } = useParams();

    return (
        <GroupTypeModelLargeFetching {...props} id={id} />
    )    

}  