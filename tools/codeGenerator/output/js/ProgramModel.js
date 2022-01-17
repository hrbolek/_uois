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
export const QueryProgramModelByidLarge = (id) => 
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
                programsById(id: ${id}) {

                    id
                    name
                    lastchange
                    externalId

                    programusermodels {
    
                        id
                        program_id
                        user_id
                        roletype_id
                    }
                    subjectmodels {
    
                        id
                        name
                        lastchange
                        externalId
                        program_id
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
export const QueryProgramModelByidMedium = (id) => 
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
                programsById(id: ${id}) {
                    id
                    name
                    lastchange
                    externalId
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/programs';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const ProgramModelSmall = (props) =>  {
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
export const ProgramModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of ProgramModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">lastchange : { props.lastchange }</li>
                    <li class="list-group-item">externalId : { props.externalId }</li>
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
 * @return 
 */
export const ProgramModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
            <td>{ props.lastchange }</td>
            <td>{ props.externalId }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const ProgramModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th><ProgramModelSmall {...props} /></th>
            <th>name</th>
            <th>lastchange</th>
            <th>externalId</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of ProgramModel
 * @return 
 */
export const ProgramModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <ProgramModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <ProgramModelTableHeadRow />
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
export const ProgramModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <ProgramModelMedium {...props}> 
                </ProgramModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const ProgramModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryProgramModelByidLarge, (response) => response.data.ProgramModel, [props.id])

    if (state !== null) {
        return <ProgramModelLarge {...state} />
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
export const ProgramModelPage = (props) => {
    const { id } = useParams();

    return (
        <ProgramModelLargeFetching {...props} id={id} />
    )    

}  