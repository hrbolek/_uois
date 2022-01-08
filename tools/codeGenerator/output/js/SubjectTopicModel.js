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
export const QuerySubjectTopicModelByidLarge = (id) => 
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
                SubjectTopicModel(id: ${id}) {

                    id
                    name
                    externalId
                    subjectsemester_id

                    subjectsemestermodel {
    
                        id
                        name
                        lastchange
                        subject_id
                    }
                    subjecttopicusermodel_collection {
    
                        id
                        subjecttopic_id
                        user_id
                        roletype_id
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
export const QuerySubjectTopicModelByidMedium = (id) => 
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
                SubjectTopicModel(id: ${id}) {
                    id
                    name
                    externalId
                    subjectsemester_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/SubjectTopicModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const SubjectTopicModelSmall = (props) =>  {
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
export const SubjectTopicModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of SubjectTopicModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">externalId : { props.externalId }</li>
                    <li class="list-group-item">subjectsemester_id : { props.subjectsemester_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @param props.externalId
 * @param props.subjectsemester_id
 * @return 
 */
export const SubjectTopicModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
            <td>{ props.externalId }</td>
            <td>{ props.subjectsemester_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const SubjectTopicModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>name</th>
            <th>externalId</th>
            <th>subjectsemester_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of SubjectTopicModel
 * @return 
 */
export const SubjectTopicModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <SubjectTopicModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <SubjectTopicModelTableHeadRow />
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
export const SubjectTopicModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <SubjectTopicModelMedium {...props}> 
                </SubjectTopicModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const SubjectTopicModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QuerySubjectTopicModelByidLarge, (response) => response.data.SubjectTopicModel, [props.id])

    if (state !== null) {
        return <SubjectTopicModelLarge {...state} />
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
export const SubjectTopicModelPage = (props) => {
    const { id } = useParams();

    return (
        <SubjectTopicModelLargeFetching {...props} id={id} />
    )    

}  