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
export const QuerySubjectSemesterModelByidLarge = (id) => 
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
                SubjectSemesterModel(id: ${id}) {

                    id
                    name
                    lastchange
                    subject_id

                    subjectmodel {
    
                        id
                        name
                        lastchange
                        externalId
                        program_id
                    }
                    subjecttopicmodel_collection {
    
                        id
                        name
                        externalId
                        subjectsemester_id
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
export const QuerySubjectSemesterModelByidMedium = (id) => 
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
                SubjectSemesterModel(id: ${id}) {
                    id
                    name
                    lastchange
                    subject_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/SubjectSemesterModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const SubjectSemesterModelSmall = (props) =>  {
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
export const SubjectSemesterModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of SubjectSemesterModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">lastchange : { props.lastchange }</li>
                    <li class="list-group-item">subject_id : { props.subject_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @param props.lastchange
 * @param props.subject_id
 * @return 
 */
export const SubjectSemesterModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
            <td>{ props.lastchange }</td>
            <td>{ props.subject_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const SubjectSemesterModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>name</th>
            <th>lastchange</th>
            <th>subject_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of SubjectSemesterModel
 * @return 
 */
export const SubjectSemesterModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <SubjectSemesterModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <SubjectSemesterModelTableHeadRow />
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
export const SubjectSemesterModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <SubjectSemesterModelMedium {...props}> 
                </SubjectSemesterModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const SubjectSemesterModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QuerySubjectSemesterModelByidLarge, (response) => response.data.SubjectSemesterModel, [props.id])

    if (state !== null) {
        return <SubjectSemesterModelLarge {...state} />
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
export const SubjectSemesterModelPage = (props) => {
    const { id } = useParams();

    return (
        <SubjectSemesterModelLargeFetching {...props} id={id} />
    )    

}  