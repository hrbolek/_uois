import {
    Link,
    useParams
  } from "react-router-dom";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';
import { GroupSmall } from '../group/group';
import { TimeTableMedium } from '../timetable/timetable';

import { root, rootGQL } from '../index';
import { useQueryGQL } from "../index";
import { Loading, LoadingError } from "../index";
const userRoot = root + '/users'


export const QueryUserByIdLarge = (id) => 
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
                user(id: ${id}) {
                    id
                    name
                    surname
                    email
                    faculties: groupsByType(typeId: 2) {
                        id
                        name
                    }
                    departments: groupsByType(typeId: 1) {
                        id
                        name
                    }
                    studyGroups: groupsByType(typeId: 3) {
                        id
                        name
                    }
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });

export const QueryUserByIdMedium = (id) => 
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
                user(id: ${id}) {
                    id
                    name
                    surname
                    email
                }
            }
            `        
        }) // body data type must match "Content-Type" header
    });

export const UserSmall = (props) => {
    return (
        <Link to={userRoot + `/${props.id}`}>{props.name}{props.children}</Link>
    )
}

export const UserSmallWithFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryUserByIdMedium, (response) => response.data.user, [props.id])
    if (state !== null) {
        return <UserSmall {...state} />
    } else if (error !== null) {
        return <LoadingError error={error} />
    } else {
        return <Loading>Uživatel {props.id}</Loading>
    }
}

export const UserLarge = (props) =>  {

    const listIntoGroupItems = (list) => {
        let result = ''
        if (list.length == 1) {
            result = <GroupSmall {...list[0]} />
        } else if (list.length > 1) {
            let items = []
            let index = 0
            for (let f of list) {
                items.push(<GroupSmall key={index} {...f} />)
                items.push(<br key={index+1}/>)
                index = index + 2
            }
            result = items
        }

        return result
    }

    let facultyRow = <></>
    if (props.faculties.length > 0) {
        let facultyItem = listIntoGroupItems(props.faculties)
        facultyRow = (<tr><td><b>Fakulta</b> </td><td>{facultyItem}</td></tr>)
    }
    let departmentRow = <></>
    if (props.departments.length > 0) {
        let departmentItem = listIntoGroupItems(props.departments)
        departmentRow = (<tr><td><b>Katedra</b> </td><td>{departmentItem}</td></tr>)
    }
    let studyGroupRow = <></>
    if (props.studyGroups.length > 0) {
        let studyGroupRow = listIntoGroupItems(props.studyGroups)
        studyGroupRow = (<tr><td><b>Studijní skupina</b> </td><td>{studyGroupRow}</td></tr>)
    }

    return (
        <>
        <Row>
            <Col>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>Základní informace o uživateli</Card.Title>
                        <UserSmall {...props} />
                    </Card.Header>
                    <Card.Body>
                        <Table striped bordered hover>
                            <tbody>
                                <tr><td><b>Uživatel ({props.id})</b></td><td>{props.name}</td></tr>
                                {facultyRow}
                                {departmentRow}
                                {studyGroupRow}
                            </tbody>
                        </Table>
                    </Card.Body>
                </Card>
            </Col>
        </Row>
        <Row>
            <Col>
                <TimeTableMedium type='student' id={props.id}/>
            </Col>
        </Row>
        
        </>
    ) 
}

export const UserLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, QueryUserByIdLarge, (response) => response.data.user, [props.id])

    if (state !== null) {
        return <UserLarge {...state} />
    } else if (error !== null) {
        return <LoadingError error={error} />
    } else {
        return <Loading>Uživatel {props.id}</Loading>
    }
}


export const UserPage = (props) => {
    const { id } = useParams();

    return (
        <UserLargeFetching {...props} id={id} />
    )    
}