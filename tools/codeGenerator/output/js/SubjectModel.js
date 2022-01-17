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
export const QuerySubjectModelByidLarge = (id) => 
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
                subjectsById(id: ${id}) {

                    id
                    name
                    lastchange
                    externalId
                    program_id

                    programmodel {
    
                        id
                        name
                        lastchange
                        externalId
                    }
                    subjectusermodels {
    
                        id
                        subject_id
                        user_id
                        roletype_id
                    }
                    subjectsemestermodels {
    
                        id
                        name
                        lastchange
                        subject_id
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
export const QuerySubjectModelByidMedium = (id) => 
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
                subjectsById(id: ${id}) {
                    id
                    name
                    lastchange
                    externalId
                    program_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/subjects';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const SubjectModelSmall = (props) =>  {
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
export const SubjectModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of SubjectModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">lastchange : { props.lastchange }</li>
                    <li class="list-group-item">externalId : { props.externalId }</li>
                    <li class="list-group-item">program_id : { props.program_id }</li>
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
 * @param props.program_id
 * @return 
 */
export const SubjectModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
            <td>{ props.lastchange }</td>
            <td>{ props.externalId }</td>
            <td>{ props.program_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const SubjectModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th><SubjectModelSmall {...props} /></th>
            <th>name</th>
            <th>lastchange</th>
            <th>externalId</th>
            <th>program_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of SubjectModel
 * @return 
 */
export const SubjectModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <SubjectModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <SubjectModelTableHeadRow />
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
export const SubjectModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <SubjectModelMedium {...props}> 
                </SubjectModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const SubjectModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QuerySubjectModelByidLarge, (response) => response.data.SubjectModel, [props.id])

    if (state !== null) {
        return <SubjectModelLarge {...state} />
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
export const SubjectModelPage = (props) => {
    const { id } = useParams();

    return (
        <SubjectModelLargeFetching {...props} id={id} />
    )    

}  