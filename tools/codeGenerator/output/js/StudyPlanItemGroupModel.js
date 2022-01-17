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
export const QueryStudyPlanItemGroupModelByidLarge = (id) => 
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
                studyplanitem_groupsById(id: ${id}) {

                    id
                    group_id
                    studyplanitem_id

                    studyplanitemmodel {
    
                        id
                        name
                        priority
                        subjectSemesterTopic
                        externalId
                        studyplan_id
                    }
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
export const QueryStudyPlanItemGroupModelByidMedium = (id) => 
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
                studyplanitem_groupsById(id: ${id}) {
                    id
                    group_id
                    studyplanitem_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/studyplanitem_groups';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const StudyPlanItemGroupModelSmall = (props) =>  {
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
export const StudyPlanItemGroupModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of StudyPlanItemGroupModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">group_id : { props.group_id }</li>
                    <li class="list-group-item">studyplanitem_id : { props.studyplanitem_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.group_id
 * @param props.studyplanitem_id
 * @return 
 */
export const StudyPlanItemGroupModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.group_id }</td>
            <td>{ props.studyplanitem_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const StudyPlanItemGroupModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th><StudyPlanItemGroupModelSmall {...props} /></th>
            <th>group_id</th>
            <th>studyplanitem_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of StudyPlanItemGroupModel
 * @return 
 */
export const StudyPlanItemGroupModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <StudyPlanItemGroupModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <StudyPlanItemGroupModelTableHeadRow />
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
export const StudyPlanItemGroupModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <StudyPlanItemGroupModelMedium {...props}> 
                </StudyPlanItemGroupModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const StudyPlanItemGroupModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryStudyPlanItemGroupModelByidLarge, (response) => response.data.StudyPlanItemGroupModel, [props.id])

    if (state !== null) {
        return <StudyPlanItemGroupModelLarge {...state} />
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
export const StudyPlanItemGroupModelPage = (props) => {
    const { id } = useParams();

    return (
        <StudyPlanItemGroupModelLargeFetching {...props} id={id} />
    )    

}  