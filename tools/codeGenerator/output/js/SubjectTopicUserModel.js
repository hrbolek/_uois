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
export const QuerySubjectTopicUserModelByidLarge = (id) => 
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
                subjecttopics_usersById(id: ${id}) {

                    id
                    subjecttopic_id
                    user_id
                    roletype_id

                    subjecttopicmodel {
    
                        id
                        name
                        externalId
                        subjectsemester_id
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
                    acreditationuserroletypemodel {
    
                        id
                        name
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
export const QuerySubjectTopicUserModelByidMedium = (id) => 
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
                subjecttopics_usersById(id: ${id}) {
                    id
                    subjecttopic_id
                    user_id
                    roletype_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/subjecttopics_users';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const SubjectTopicUserModelSmall = (props) =>  {
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
export const SubjectTopicUserModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of SubjectTopicUserModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">subjecttopic_id : { props.subjecttopic_id }</li>
                    <li class="list-group-item">user_id : { props.user_id }</li>
                    <li class="list-group-item">roletype_id : { props.roletype_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.subjecttopic_id
 * @param props.user_id
 * @param props.roletype_id
 * @return 
 */
export const SubjectTopicUserModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.subjecttopic_id }</td>
            <td>{ props.user_id }</td>
            <td>{ props.roletype_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const SubjectTopicUserModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th><SubjectTopicUserModelSmall {...props} /></th>
            <th>subjecttopic_id</th>
            <th>user_id</th>
            <th>roletype_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of SubjectTopicUserModel
 * @return 
 */
export const SubjectTopicUserModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <SubjectTopicUserModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <SubjectTopicUserModelTableHeadRow />
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
export const SubjectTopicUserModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <SubjectTopicUserModelMedium {...props}> 
                </SubjectTopicUserModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const SubjectTopicUserModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QuerySubjectTopicUserModelByidLarge, (response) => response.data.SubjectTopicUserModel, [props.id])

    if (state !== null) {
        return <SubjectTopicUserModelLarge {...state} />
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
export const SubjectTopicUserModelPage = (props) => {
    const { id } = useParams();

    return (
        <SubjectTopicUserModelLargeFetching {...props} id={id} />
    )    

}  