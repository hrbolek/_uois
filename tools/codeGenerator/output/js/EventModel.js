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
export const QueryEventModelByidLarge = (id) => 
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
                EventModel(id: ${id}) {

                    id
                    start
                    end
                    label
                    externalId
                    lastchange

                    eventusermodel_collection {
    
                        id
                        user_id
                        event_id
                    }
                    eventgroupmodel_collection {
    
                        id
                        group_id
                        event_id
                    }
                    studyplanitemeventmodel_collection {
    
                        id
                        studyplanitem_id
                        event_id
                    }
                    eventroommodel_collection {
    
                        id
                        room_id
                        event_id
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
export const QueryEventModelByidMedium = (id) => 
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
                EventModel(id: ${id}) {
                    id
                    start
                    end
                    label
                    externalId
                    lastchange
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });    

const entityRoot = root + '/EventModel';

/*
 * @param props.id unique identification
 * @param props.name visual representation of item
 * @param props.label visual representation of item
 * @param props.children embeded items
 * @return 
 */
export const EventModelSmall = (props) =>  {
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
export const EventModelMedium = (props) =>  {
    return (
        <Card>
            <Card.Header className='bg-success bg-gradient text-white'>
                <Card.Title>Title of EventModel</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul class="list-group">
                    <li class="list-group-item">id : { props.id }</li>
                    <li class="list-group-item">start : { props.start }</li>
                    <li class="list-group-item">end : { props.end }</li>
                    <li class="list-group-item">label : { props.label }</li>
                    <li class="list-group-item">externalId : { props.externalId }</li>
                    <li class="list-group-item">lastchange : { props.lastchange }</li>
                </ul>
            </Card.Body>
        </Card>
    ) 
}

/*
 * @param props.id
 * @param props.start
 * @param props.end
 * @param props.label
 * @param props.externalId
 * @param props.lastchange
 * @return 
 */
export const EventModelTableRow = (props) =>  {
    return (
        <tr>
            <td>{ props.id }</td>
            <td>{ props.start }</td>
            <td>{ props.end }</td>
            <td>{ props.label }</td>
            <td>{ props.externalId }</td>
            <td>{ props.lastchange }</td>
        </tr>
    ) 
}

/*
 * @return 
 */
export const EventModelTableHeadRow = (props) =>  {
    return (
        <tr>
            <th>id</th>
            <th>start</th>
            <th>end</th>
            <th>label</th>
            <th>externalId</th>
            <th>lastchange</th>
        </tr>
    ) 
}

/*
 * @param props.data is array of EventModel
 * @return 
 */
export const EventModelTable = (props) =>  {
    const rows = props.data.map(
        (item, index) => <EventModelTableRow key={'k' + index} {...item}/>
        );

    return (
        <Table>
            <thead>
                <EventModelTableHeadRow />
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
export const EventModelLarge = (props) =>  {
    return (
        <>
        <Row>
            <Col>
                <EventModelMedium {...props}> 
                </EventModelMedium> 
            </Col>
        </Row>
        </>
    ) 
}

/*
 * @param props holds all data needed for proper rendering
 * @return 
 */
export const EventModelLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryEventModelByidLarge, (response) => response.data.EventModel, [props.id])

    if (state !== null) {
        return <EventModelLarge {...state} />
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
export const EventModelPage = (props) => {
    const { id } = useParams();

    return (
        <EventModelLargeFetching {...props} id={id} />
    )    

}  