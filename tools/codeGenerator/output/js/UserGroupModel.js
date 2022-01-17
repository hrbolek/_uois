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
export const QueryUserGroupModelByidLarge = (id) => 
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
                users_groupsById(id: ${id}) {

                    id
                    user_id
                    group_id

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
export const QueryUserGroupModelByidMedium = (id) => 
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
                users_groupsById(id: ${id}) {
                    id
                    user_id
                    group_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/users_groups';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const UserGroupModelSmall = (props) =>  {
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
export const UserGroupModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of UserGroupModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">user_id : { props.user_id }</li>
                    <li class="list-group-item">group_id : { props.group_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.user_id
 * @param props.group_id
 * @return 
 */
export const UserGroupModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.user_id }</td>
            <td>{ props.group_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const UserGroupModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th><UserGroupModelSmall {...props} /></th>
            <th>user_id</th>
            <th>group_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of UserGroupModel
 * @return 
 */
export const UserGroupModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <UserGroupModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <UserGroupModelTableHeadRow />
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
export const UserGroupModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <UserGroupModelMedium {...props}> 
                </UserGroupModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const UserGroupModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryUserGroupModelByidLarge, (response) => response.data.UserGroupModel, [props.id])

    if (state !== null) {
        return <UserGroupModelLarge {...state} />
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
export const UserGroupModelPage = (props) => {
    const { id } = useParams();

    return (
        <UserGroupModelLargeFetching {...props} id={id} />
    )    

}  