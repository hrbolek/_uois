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
export const QueryAcreditationUserRoleTypeModelByidLarge = (id) => 
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
                AcreditationUserRoleTypeModel(id: ${id}) {

                    id
                    name

                    programusermodel_collection {
    
                        id
                        program_id
                        user_id
                        roletype_id
                    }
                    subjectusermodel_collection {
    
                        id
                        subject_id
                        user_id
                        roletype_id
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
export const QueryAcreditationUserRoleTypeModelByidMedium = (id) => 
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
                AcreditationUserRoleTypeModel(id: ${id}) {
                    id
                    name
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/AcreditationUserRoleTypeModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const AcreditationUserRoleTypeModelSmall = (props) =>  {
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
export const AcreditationUserRoleTypeModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of AcreditationUserRoleTypeModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">name : { props.name }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.name
 * @return 
 */
export const AcreditationUserRoleTypeModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.name }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const AcreditationUserRoleTypeModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>name</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of AcreditationUserRoleTypeModel
 * @return 
 */
export const AcreditationUserRoleTypeModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <AcreditationUserRoleTypeModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <AcreditationUserRoleTypeModelTableHeadRow />
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
export const AcreditationUserRoleTypeModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <AcreditationUserRoleTypeModelMedium {...props}> 
                </AcreditationUserRoleTypeModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const AcreditationUserRoleTypeModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryAcreditationUserRoleTypeModelByidLarge, (response) => response.data.AcreditationUserRoleTypeModel, [props.id])

    if (state !== null) {
        return <AcreditationUserRoleTypeModelLarge {...state} />
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
export const AcreditationUserRoleTypeModelPage = (props) => {
    const { id } = useParams();

    return (
        <AcreditationUserRoleTypeModelLargeFetching {...props} id={id} />
    )    

}  