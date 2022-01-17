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
export const QueryStudyPlanItemModelByidLarge = (id) => 
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
                studyplanitemsById(id: ${id}) {

                    id
                    name
                    priority
                    subjectSemesterTopic
                    externalId
                    studyplan_id

                    studyplanmodel {
    
                        id
                        name
                        externalId
                    }
                    studyplanitemeventmodels {
    
                        id
                        studyplanitem_id
                        event_id
                    }
                    studyplanitemteachermodels {
    
                        id
                        teacher_id
                        studyplanitem_id
                    }
                    studyplanitemgroupmodels {
    
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
export const QueryStudyPlanItemModelByidMedium = (id) => 
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
                studyplanitemsById(id: ${id}) {
                    id
                    name
                    priority
                    subjectSemesterTopic
                    externalId
                    studyplan_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/studyplanitems';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const StudyPlanItemModelSmall = (props) =>  {
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
export const StudyPlanItemModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of StudyPlanItemModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">priority : { props.priority }</li>
                    <li class="list-group-item">subjectSemesterTopic : { props.subjectSemesterTopic }</li>
                    <li class="list-group-item">externalId : { props.externalId }</li>
                    <li class="list-group-item">studyplan_id : { props.studyplan_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @param props.priority
 * @param props.subjectSemesterTopic
 * @param props.externalId
 * @param props.studyplan_id
 * @return 
 */
export const StudyPlanItemModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
            <td>{ props.priority }</td>
            <td>{ props.subjectSemesterTopic }</td>
            <td>{ props.externalId }</td>
            <td>{ props.studyplan_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const StudyPlanItemModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th><StudyPlanItemModelSmall {...props} /></th>
            <th>name</th>
            <th>priority</th>
            <th>subjectSemesterTopic</th>
            <th>externalId</th>
            <th>studyplan_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of StudyPlanItemModel
 * @return 
 */
export const StudyPlanItemModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <StudyPlanItemModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <StudyPlanItemModelTableHeadRow />
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
export const StudyPlanItemModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <StudyPlanItemModelMedium {...props}> 
                </StudyPlanItemModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const StudyPlanItemModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryStudyPlanItemModelByidLarge, (response) => response.data.StudyPlanItemModel, [props.id])

    if (state !== null) {
        return <StudyPlanItemModelLarge {...state} />
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
export const StudyPlanItemModelPage = (props) => {
    const { id } = useParams();

    return (
        <StudyPlanItemModelLargeFetching {...props} id={id} />
    )    

}  