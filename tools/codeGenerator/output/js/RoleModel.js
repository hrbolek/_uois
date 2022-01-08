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
export const QueryRoleModelByidLarge = (id) => 
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
                RoleModel(id: ${id}) {

                    id
                    name
                    lastchange
                    roletype_id
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
                    roletypemodel {
    
                        id
                        name
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
export const QueryRoleModelByidMedium = (id) => 
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
                RoleModel(id: ${id}) {
                    id
                    name
                    lastchange
                    roletype_id
                    user_id
                    group_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/RoleModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const RoleModelSmall = (props) =>  {
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
export const RoleModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of RoleModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                    <li class="list-group-item">lastchange : { props.lastchange }</li>
                    <li class="list-group-item">roletype_id : { props.roletype_id }</li>
                    <li class="list-group-item">user_id : { props.user_id }</li>
                    <li class="list-group-item">group_id : { props.group_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @param props.lastchange
 * @param props.roletype_id
 * @param props.user_id
 * @param props.group_id
 * @return 
 */
export const RoleModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
            <td>{ props.lastchange }</td>
            <td>{ props.roletype_id }</td>
            <td>{ props.user_id }</td>
            <td>{ props.group_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const RoleModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>name</th>
            <th>lastchange</th>
            <th>roletype_id</th>
            <th>user_id</th>
            <th>group_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of RoleModel
 * @return 
 */
export const RoleModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <RoleModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <RoleModelTableHeadRow />
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
export const RoleModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <RoleModelMedium {...props}> 
                </RoleModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const RoleModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryRoleModelByidLarge, (response) => response.data.RoleModel, [props.id])

    if (state !== null) {
        return <RoleModelLarge {...state} />
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
export const RoleModelPage = (props) => {
    const { id } = useParams();

    return (
        <RoleModelLargeFetching {...props} id={id} />
    )    

}  