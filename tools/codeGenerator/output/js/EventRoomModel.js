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
export const QueryEventRoomModelByidLarge = (id) => 
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
                EventRoomModel(id: ${id}) {

                    id
                    room_id
                    event_id

                    roommodel {
    
                        id
                        name
                        lastchange
                        externalId
                        building_id
                    }
                    eventmodel {
    
                        id
                        start
                        end
                        label
                        externalId
                        lastchange
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
export const QueryEventRoomModelByidMedium = (id) => 
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
                EventRoomModel(id: ${id}) {
                    id
                    room_id
                    event_id
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/EventRoomModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const EventRoomModelSmall = (props) =>  {
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
export const EventRoomModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of EventRoomModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">room_id : { props.room_id }</li>
                    <li class="list-group-item">event_id : { props.event_id }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.room_id
 * @param props.event_id
 * @return 
 */
export const EventRoomModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.room_id }</td>
            <td>{ props.event_id }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const EventRoomModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>room_id</th>
            <th>event_id</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of EventRoomModel
 * @return 
 */
export const EventRoomModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <EventRoomModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <EventRoomModelTableHeadRow />
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
export const EventRoomModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <EventRoomModelMedium {...props}> 
                </EventRoomModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const EventRoomModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryEventRoomModelByidLarge, (response) => response.data.EventRoomModel, [props.id])

    if (state !== null) {
        return <EventRoomModelLarge {...state} />
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
export const EventRoomModelPage = (props) => {
    const { id } = useParams();

    return (
        <EventRoomModelLargeFetching {...props} id={id} />
    )    

}  