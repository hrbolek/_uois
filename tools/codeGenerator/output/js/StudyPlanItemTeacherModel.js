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
export const QueryStudyPlanItemTeacherModelByidLarge = (id) => 
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
                StudyPlanItemTeacherModel(id: ${id}) {

                    id
                    teacher_id
                    studyplanitem_id

                    studyplanitemmodel {
    
                        id
                        name
                        priority
                        subjectSemesterTopic
                        externalId
                        studyplan_id
                    }
                    usermodel {
    
                        id
                        name
                        surname
                        email
                        lastchange
                        externalId
                        UCO
                        VaVId
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
export const QueryStudyPlanItemTeacherModelByidMedium = (id) => 
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
                StudyPlanItemTeacherModel(id: ${id}) {
                    id
                    teacher_id
                    studyplanitem_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/StudyPlanItemTeacherModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const StudyPlanItemTeacherModelSmall = (props) =>  {
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
export const StudyPlanItemTeacherModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of StudyPlanItemTeacherModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">teacher_id : { props.teacher_id }</li>
                    <li class="list-group-item">studyplanitem_id : { props.studyplanitem_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.teacher_id
 * @param props.studyplanitem_id
 * @return 
 */
export const StudyPlanItemTeacherModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.teacher_id }</td>
            <td>{ props.studyplanitem_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const StudyPlanItemTeacherModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>teacher_id</th>
            <th>studyplanitem_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of StudyPlanItemTeacherModel
 * @return 
 */
export const StudyPlanItemTeacherModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <StudyPlanItemTeacherModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <StudyPlanItemTeacherModelTableHeadRow />
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
export const StudyPlanItemTeacherModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <StudyPlanItemTeacherModelMedium {...props}> 
                </StudyPlanItemTeacherModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const StudyPlanItemTeacherModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryStudyPlanItemTeacherModelByidLarge, (response) => response.data.StudyPlanItemTeacherModel, [props.id])

    if (state !== null) {
        return <StudyPlanItemTeacherModelLarge {...state} />
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
export const StudyPlanItemTeacherModelPage = (props) => {
    const { id } = useParams();

    return (
        <StudyPlanItemTeacherModelLargeFetching {...props} id={id} />
    )    

}  