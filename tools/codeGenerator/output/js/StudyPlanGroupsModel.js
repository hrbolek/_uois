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
export const QueryStudyPlanGroupsModelByidLarge = (id) => 
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
                StudyPlanGroupsModel(id: ${id}) {

                    id
                    studyplan_id
                    group_id

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
                    studyplanmodel {
    
                        id
                        name
                        externalId
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
export const QueryStudyPlanGroupsModelByidMedium = (id) => 
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
                StudyPlanGroupsModel(id: ${id}) {
                    id
                    studyplan_id
                    group_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/StudyPlanGroupsModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const StudyPlanGroupsModelSmall = (props) =>  {
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
export const StudyPlanGroupsModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of StudyPlanGroupsModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">studyplan_id : { props.studyplan_id }</li>
                    <li class="list-group-item">group_id : { props.group_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.studyplan_id
 * @param props.group_id
 * @return 
 */
export const StudyPlanGroupsModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.studyplan_id }</td>
            <td>{ props.group_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const StudyPlanGroupsModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>studyplan_id</th>
            <th>group_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of StudyPlanGroupsModel
 * @return 
 */
export const StudyPlanGroupsModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <StudyPlanGroupsModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <StudyPlanGroupsModelTableHeadRow />
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
export const StudyPlanGroupsModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <StudyPlanGroupsModelMedium {...props}> 
                </StudyPlanGroupsModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const StudyPlanGroupsModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryStudyPlanGroupsModelByidLarge, (response) => response.data.StudyPlanGroupsModel, [props.id])

    if (state !== null) {
        return <StudyPlanGroupsModelLarge {...state} />
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
export const StudyPlanGroupsModelPage = (props) => {
    const { id } = useParams();

    return (
        <StudyPlanGroupsModelLargeFetching {...props} id={id} />
    )    

}  