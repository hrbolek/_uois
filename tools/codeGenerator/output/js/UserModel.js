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
export const QueryUserModelByidLarge = (id) => 
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
                UserModel(id: ${id}) {

                    id
                    name
                    surname
                    email
                    lastchange
                    externalId
                    UCO
                    VaVId

                    eventusermodel_collection {
    
                        id
                        user_id
                        event_id
                    }
                    programusermodel_collection {
    
                        id
                        program_id
                        user_id
                        roletype_id
                    }
                    usergroupmodel_collection {
    
                        id
                        user_id
                        group_id
                    }
                    rolemodel_collection {
    
                        id
                        name
                        lastchange
                        roletype_id
                        user_id
                        group_id
                    }
                    subjectusermodel_collection {
    
                        id
                        subject_id
                        user_id
                        roletype_id
                    }
                    studyplanitemteachermodel_collection {
    
                        id
                        teacher_id
                        studyplanitem_id
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
export const QueryUserModelByidMedium = (id) => 
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
                UserModel(id: ${id}) {
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
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/UserModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const UserModelSmall = (props) =>  {
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
export const UserModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of UserModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">surname : { props.surname }</li>
                    <li class="list-group-item">email : { props.email }</li>
                    <li class="list-group-item">lastchange : { props.lastchange }</li>
                    <li class="list-group-item">externalId : { props.externalId }</li>
                    <li class="list-group-item">UCO : { props.UCO }</li>
                    <li class="list-group-item">VaVId : { props.VaVId }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @param props.surname
 * @param props.email
 * @param props.lastchange
 * @param props.externalId
 * @param props.UCO
 * @param props.VaVId
 * @return 
 */
export const UserModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
            <td>{ props.surname }</td>
            <td>{ props.email }</td>
            <td>{ props.lastchange }</td>
            <td>{ props.externalId }</td>
            <td>{ props.UCO }</td>
            <td>{ props.VaVId }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const UserModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>name</th>
            <th>surname</th>
            <th>email</th>
            <th>lastchange</th>
            <th>externalId</th>
            <th>UCO</th>
            <th>VaVId</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of UserModel
 * @return 
 */
export const UserModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <UserModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <UserModelTableHeadRow />
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
export const UserModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <UserModelMedium {...props}> 
                </UserModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const UserModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryUserModelByidLarge, (response) => response.data.UserModel, [props.id])

    if (state !== null) {
        return <UserModelLarge {...state} />
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
export const UserModelPage = (props) => {
    const { id } = useParams();

    return (
        <UserModelLargeFetching {...props} id={id} />
    )    

}  