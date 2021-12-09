import {
    Link,
    useParams
  } from "react-router-dom";
import { useEffect, useState } from "react";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import CloseButton from 'react-bootstrap/CloseButton';
import Table from 'react-bootstrap/Table';

import { root } from '../index';
import { CreateExpandable } from '../../helpers/index';

import { TeacherSmall } from '../teacher/teacher';
import { GroupSmall } from '../group/group';
import { TimeTableMedium } from '../timetable/timetable';
import { SubjectSmall } from '../subject/subject';

const studentRoot = root + '/students'


export const _StudentSmall = (props) => {
    //embeded Student
    return (
        <Link to={studentRoot + `/${props.id}`}>{props.name}{props.children}</Link>
    )
}

export const StudentMedium = (props) => {
    return (
        <Card>
            {/*<Card.Img variant="top" src="holder.js/100px180" />*/}
            <Card.Body>
                <Card.Header className='bg-success bg-gradient text-white'>
                    <Card.Title>Student ID:{props.id}, {props.name}</Card.Title>
                </Card.Header>
                <Card.Text>
                FVT <br />
                Katedra <br />
                Skupina <br />
                </Card.Text>
            </Card.Body>
            {props.children}
        </Card> 
    )    
}

export const StudentLarge = (props) => {
    const [state, setState] = useState(
        {
            'id': props.id,
            'name': props.name,
            'faculty': 'FVT',
            'department': [{'id': 124, 'name': 'K209'}],
            'studyGroups': [
                {'id': 257, 'name': '23-5AT'}
            ],
            'subjects': [
                {'id': 458, 'name': 'subj1'}
            ]
        })

    useEffect(()=>{
        `
        query {
            user(id: $id$) {
                id
                externalId
                name
                surname
                fullname
                faculty: groupsByType(type: 0) {
                    id
                    name
                }
                department: groupsByType(type: 1) {
                    id
                    name
                }
                studyGroups: groupsByType(type: 2) {
                    id
                    name
                }
                studyprograms {
                    id
                    externalId
                    name
                }
            }
        }
        `

    }, [props.id])

    const studyGroups = []
    for(var index = 0; index < state.studyGroups.length; index++) {
        const sgItem = state.studyGroups[index]
        studyGroups.push(<GroupSmall id={sgItem.id} name={sgItem.name}/>);
        studyGroups.push(<br />);
    }

    const studySubjects = []
    for(var index = 0; index < state.subjects.length; index++) {
        const ssItem = state.subjects[index];
        studySubjects.push(<SubjectSmall id={ssItem.id} name={ssItem.name}/>)
    }

    return (
        <>
        <Row>
            <Col>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>Základní informace o studentovi</Card.Title>
                    </Card.Header>
                    <Card.Body>
                        <Table striped bordered hover>
                            <tbody>
                                <tr><td><b>Student ({state.id})</b></td><td>{state.name}</td></tr>
                                <tr><td><b>Fakulta</b> </td><td>{state.faculty}</td></tr>
                                <tr><td><b>Katedra</b> </td><td>{state.department}</td></tr>
                                <tr><td><b>Studijní skupina</b> </td><td>{studyGroups}</td></tr>
                                <tr><td><b>Studijní obor</b> </td><td></td></tr>
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
        
        <Row>
            <Col>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>Seznam předmětů</Card.Title>
                    </Card.Header>
                    <Card.Body>
                        {studySubjects}
                    </Card.Body>
                </Card>
            </Col>
        </Row>
        <Row>
            <Col>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>Seznam učitelů</Card.Title>
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

export const StudentPage = (props) => {
    const { id } = useParams();
    const name = 'Josef Novák'
    return (
        <StudentLarge id={id} name={name} />
    )
}

export const StudentList = (props) => {
    return (
        <div>Toto je seznam studentů</div>
    )
}

export const Students = (props) => {
    return (
        <Row>
            Studenti
            <br />
            <StudentSmall id='635' label='Petr Novak' />
            <br />
            <StudentSmall id='698' label='Petr Novak' />
            <br />
            <StudentSmall id='758' label='Petr Novak' />
        </Row>
    )
}

//<Button class="btn-close" size='sm' onClick={() => setExpanded(false)}>méně</Button>
export const StudentSmall = (props) => {
    const [expanded, setExpanded] = useState(false);
    var result = <>Error</>
    if (expanded) {
        result = (
            <>
                
                <StudentMedium {...props} >
                <span className="btn position-absolute top-0 start-0 translate-middle p-2 bg-danger border border-light rounded-circle" onClick={() => setExpanded(false)}>
                    <span className="visually-hidden">New alerts</span>
                </span>
                </StudentMedium>
            </>
        )
    } else {
        result = (
            <>
                <_StudentSmall {...props} /> 
                <span >{'\u00A0\u00A0'}</span>
                <span className="btn translate-middle bg-success border border-light rounded-circle badge bg-secondary" onClick={() => setExpanded(true)}>{'\u00A0'}</span>
            </>
        )
    }
    return result
}

//<Button size='sm' onClick={() => setExpanded(true)}>více</Button>
//<Button onClick={() => setExpanded(true)}>více</Button>
