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
export const QueryStudyPlanItemEventModelByidLarge = (id) => 
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
                studyplanitem_eventsById(id: ${id}) {

                    id
                    studyplanitem_id
                    event_id

                    eventmodel {
    
                        id
                        start
                        end
                        label
                        externalId
                        lastchange
                    }
                    studyplanitemmodel {
    
                        id
                        name
                        priority
                        subjectSemesterTopic
                        externalId
                        studyplan_id
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
export const QueryStudyPlanItemEventModelByidMedium = (id) => 
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
                studyplanitem_eventsById(id: ${id}) {
                    id
                    studyplanitem_id
                    event_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/studyplanitem_events';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const StudyPlanItemEventModelSmall = (props) =>  {
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
export const StudyPlanItemEventModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of StudyPlanItemEventModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">studyplanitem_id : { props.studyplanitem_id }</li>
                    <li class="list-group-item">event_id : { props.event_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.studyplanitem_id
 * @param props.event_id
 * @return 
 */
export const StudyPlanItemEventModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.studyplanitem_id }</td>
            <td>{ props.event_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const StudyPlanItemEventModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th><StudyPlanItemEventModelSmall {...props} /></th>
            <th>studyplanitem_id</th>
            <th>event_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of StudyPlanItemEventModel
 * @return 
 */
export const StudyPlanItemEventModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <StudyPlanItemEventModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <StudyPlanItemEventModelTableHeadRow />
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
export const StudyPlanItemEventModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <StudyPlanItemEventModelMedium {...props}> 
                </StudyPlanItemEventModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const StudyPlanItemEventModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryStudyPlanItemEventModelByidLarge, (response) => response.data.StudyPlanItemEventModel, [props.id])

    if (state !== null) {
        return <StudyPlanItemEventModelLarge {...state} />
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
export const StudyPlanItemEventModelPage = (props) => {
    const { id } = useParams();

    return (
        <StudyPlanItemEventModelLargeFetching {...props} id={id} />
    )    

}  