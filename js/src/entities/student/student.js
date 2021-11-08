import {
    Link,
    useParams
  } from "react-router-dom";
import { useState } from "react";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import CloseButton from 'react-bootstrap/CloseButton';


import { root } from '../index';
import { CreateExpandable } from '../../helpers/index';

import { TeacherSmall } from '../teacher/teacher';
import { GroupSmall } from '../group/group';
import { TimeTableMedium } from '../timetable/timetable';

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
                <Card.Title>Student ID:{props.id}, {props.name}</Card.Title>
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
    return (
        <>
        <Row>
            <Col>
                <Card>
                    <Card.Header>
                        <Card.Title>Základní informace o studentovi</Card.Title>
                    </Card.Header>
                    <Card.Body>
                    Student ID:{props.id}, {props.name} <br />
                    FVT <br />
                    Katedra <br />
                    Skupina <GroupSmall id={257} name='23-5AT' /> <br />
                    Studijní obor <br />
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
                    <Card.Header>
                        <Card.Title>Seznam předmětů</Card.Title>
                    </Card.Header>
                    <Card.Body>
                    </Card.Body>
                </Card>
            </Col>
        </Row>
        <Row>
            <Col>
                <Card>
                    <Card.Header>
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
    const name = 'fetched name'
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
