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
export const QueryProgramUserModelByidLarge = (id) => 
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
                programs_usersById(id: ${id}) {

                    id
                    program_id
                    user_id
                    roletype_id

                    acreditationuserroletypemodel {
    
                        id
                        name
                    }
                    programmodel {
    
                        id
                        name
                        lastchange
                        externalId
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
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

/*
 * @param id holds value for unique entity identification
 * @return Future with response from gQL server
 */
export const QueryProgramUserModelByidMedium = (id) => 
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
                programs_usersById(id: ${id}) {
                    id
                    program_id
                    user_id
                    roletype_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/programs_users';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const ProgramUserModelSmall = (props) =>  {
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
export const ProgramUserModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of ProgramUserModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">program_id : { props.program_id }</li>
                    <li class="list-group-item">user_id : { props.user_id }</li>
                    <li class="list-group-item">roletype_id : { props.roletype_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.program_id
 * @param props.user_id
 * @param props.roletype_id
 * @return 
 */
export const ProgramUserModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.program_id }</td>
            <td>{ props.user_id }</td>
            <td>{ props.roletype_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const ProgramUserModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th><ProgramUserModelSmall {...props} /></th>
            <th>program_id</th>
            <th>user_id</th>
            <th>roletype_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of ProgramUserModel
 * @return 
 */
export const ProgramUserModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <ProgramUserModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <ProgramUserModelTableHeadRow />
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
export const ProgramUserModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <ProgramUserModelMedium {...props}> 
                </ProgramUserModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const ProgramUserModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryProgramUserModelByidLarge, (response) => response.data.ProgramUserModel, [props.id])

    if (state !== null) {
        return <ProgramUserModelLarge {...state} />
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
export const ProgramUserModelPage = (props) => {
    const { id } = useParams();

    return (
        <ProgramUserModelLargeFetching {...props} id={id} />
    )    

}  