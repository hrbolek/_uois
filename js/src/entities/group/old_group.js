import {
    Link,
    useParams
  } from "react-router-dom";
import { useEffect, useState } from "react";

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

import { TeacherSmall } from '../teacher/teacher';
import { StudentSmall } from '../student/student';
import { UserSmall } from "../user/user";

import { root, rootGQL } from '../index'
import { useQueryGQL } from "../index";
import { Loading, LoadingError } from "../index";

const groupRoot = root + '/groups'

export const QueryGroupByIdLarge = (id) => 
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
                group(id: ${id}) {
                  id
                  name
                  grouptypeId
                  users {
                    id
                    name
                    surname
                    email
                  }
                }
              }
            `        
        }) // body data type must match "Content-Type" header
});

export const QueryGroupByIdMedium = (id) => 
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
                group(id: ${id}) {
                  id
                  name
                  grouptypeId
                }
              }
            `        
        }) // body data type must match "Content-Type" header
});

export const GroupSmall = (props) => {
    //embeded Student
    return (
        <Link to={groupRoot + `/${props.id}`}>{props.name}</Link>
    )
}
    
export const GroupSmallWithFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryGroupByIdMedium, (response) => response.data.group, [props.id])
    if (state !== null) {
        return <GroupSmall {...state} />
    } else if (error !== null) {
        return <LoadingError error={error} />
    } else {
        return <Loading>Skupina {props.id}</Loading>
    }
}

export const GroupMedium = (props) => {
    return (
        <Card>
            {/*<Card.Img variant="top" src="holder.js/100px180" />*/}
            <Card.Body>
                <Card.Title>Skupina ID:{props.id}, {props.name}</Card.Title>
                <Card.Text>
                </Card.Text>
            </Card.Body>
        </Card>            
    )
}

export const GroupMediumWithFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryGroupByIdMedium, (response) => response.data.group, [props.id])
    if (state !== null) {
        return <GroupMedium {...state} />
    } else if (error !== null) {
        return <LoadingError error={error} />
    } else {
        return <Loading>Skupina {props.id}</Loading>
    }
}

export const GroupLarge = (props) => {
    let users = props.users.map((item, index) => (<><UserSmall key={index} {...item} /><br key={'k' + index} /></>))

    return (
        <>
        <Row>
            <Col>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>Základní informace</Card.Title>
                    </Card.Header>
                    <Card.Body>
                        Skupina ID:{props.id}, {props.name}<br />
                        <a href={'mailto:student1@unob.cz?cc=student2@unob.cz;student3@unob.cz&subject=Email z IS'}>@</a> <br />
                        Typ : {props.grouptypeId}
                    </Card.Body>
                </Card>
            </Col>
        </Row>
        <Row>
            <Col>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>Příslušníci:</Card.Title>
                    </Card.Header>
                    <Card.Body>
                        {users}
                    </Card.Body>
                </Card>
            </Col>
            
        </Row>
        <Row>
            <Col>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>Vyučující:</Card.Title>
                    </Card.Header>
                    <Card.Body>
                        <TeacherSmall id='633' name='Štefek' /><br />
                        <TeacherSmall id='633' name='Štefek' /><br />
                    </Card.Body>
                </Card>
            </Col>
            
        </Row>
        </>
    )
}

export const GroupLargeWithFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryGroupByIdLarge, (response) => response.data.group, [props.id])
    if (state !== null) {
        return <GroupLarge {...state} />
    } else if (error !== null) {
        return <LoadingError error={error} />
    } else {
        return <Loading>Skupina {props.id}</Loading>
    }
}

export const GroupPage = (props) => {
    const { id } = useParams();

    return (
        <GroupLargeWithFetching id={id} />
    )
}

export const GroupList = (props) => {
    return (
        <div>Toto je seznam skupin</div>
    )
}