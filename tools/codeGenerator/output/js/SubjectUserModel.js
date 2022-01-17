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
export const QuerySubjectUserModelByidLarge = (id) => 
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
                subjects_usersById(id: ${id}) {

                    id
                    subject_id
                    user_id
                    roletype_id

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
                    subjectmodel {
    
                        id
                        name
                        lastchange
                        externalId
                        program_id
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
export const QuerySubjectUserModelByidMedium = (id) => 
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
                subjects_usersById(id: ${id}) {
                    id
                    subject_id
                    user_id
                    roletype_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/subjects_users';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const SubjectUserModelSmall = (props) =>  {
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
export const SubjectUserModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of SubjectUserModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">subject_id : { props.subject_id }</li>
                    <li class="list-group-item">user_id : { props.user_id }</li>
                    <li class="list-group-item">roletype_id : { props.roletype_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.subject_id
 * @param props.user_id
 * @param props.roletype_id
 * @return 
 */
export const SubjectUserModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.subject_id }</td>
            <td>{ props.user_id }</td>
            <td>{ props.roletype_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const SubjectUserModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th><SubjectUserModelSmall {...props} /></th>
            <th>subject_id</th>
            <th>user_id</th>
            <th>roletype_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of SubjectUserModel
 * @return 
 */
export const SubjectUserModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <SubjectUserModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <SubjectUserModelTableHeadRow />
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
export const SubjectUserModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <SubjectUserModelMedium {...props}> 
                </SubjectUserModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const SubjectUserModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QuerySubjectUserModelByidLarge, (response) => response.data.SubjectUserModel, [props.id])

    if (state !== null) {
        return <SubjectUserModelLarge {...state} />
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
export const SubjectUserModelPage = (props) => {
    const { id } = useParams();

    return (
        <SubjectUserModelLargeFetching {...props} id={id} />
    )    

}  