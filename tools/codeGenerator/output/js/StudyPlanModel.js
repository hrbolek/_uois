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
export const QueryStudyPlanModelByidLarge = (id) => 
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
                StudyPlanModel(id: ${id}) {

                    id
                    name
                    externalId

                    studyplanitemmodel_collection {
    
                        id
                        name
                        priority
                        subjectSemesterTopic
                        externalId
                        studyplan_id
                    }
                    studyplangroupsmodel_collection {
    
                        id
                        studyplan_id
                        group_id
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
export const QueryStudyPlanModelByidMedium = (id) => 
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
                StudyPlanModel(id: ${id}) {
                    id
                    name
                    externalId
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/StudyPlanModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const StudyPlanModelSmall = (props) =>  {
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
export const StudyPlanModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of StudyPlanModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">externalId : { props.externalId }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @param props.externalId
 * @return 
 */
export const StudyPlanModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
            <td>{ props.externalId }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const StudyPlanModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>name</th>
            <th>externalId</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of StudyPlanModel
 * @return 
 */
export const StudyPlanModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <StudyPlanModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <StudyPlanModelTableHeadRow />
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
export const StudyPlanModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <StudyPlanModelMedium {...props}> 
                </StudyPlanModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const StudyPlanModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryStudyPlanModelByidLarge, (response) => response.data.StudyPlanModel, [props.id])

    if (state !== null) {
        return <StudyPlanModelLarge {...state} />
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
export const StudyPlanModelPage = (props) => {
    const { id } = useParams();

    return (
        <StudyPlanModelLargeFetching {...props} id={id} />
    )    

}  