import {
    Link,
    useParams
  } from "react-router-dom";
import { useEffect, useState } from "react";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

import { TeacherSmall } from '../teacher/teacher';
import { TimeTableMedium } from '../timetable/timetable';

import { root } from '../index';
const subjectRoot = root + '/subjects';

export const SubjectSmall = (props) => {
    return (
        <Link to={subjectRoot + `/${props.id}`}>{props.name}{props.children}</Link>
    )
}

export const SubjectLarge = (props) => {
    const [state, setState] = useState({
        'id': props.id,
        'name': props.name,
        'faculty': 'FVT',
        'department': 'K209',
        'garant': {'id': 633, name: 'Alexandr Štefek'},
        'x': {}
    })

    useEffect(() => {

    })

    return (
        <>
        <Row>
            <Col>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>Základní informace o předmětu</Card.Title>
                    </Card.Header>
                    <Card.Body>
                        Předmět ID:{state.id}, {state.name} <br />
                        Fakulta {state.faculty}<br />
                        Katedra {state.department} <br />
                        
                        Studijní obor <br />
                        Garant <TeacherSmall id={state.garant.id} name={state.garant.name}/><br />
                        Zástupce garanta <TeacherSmall id={state.garant.id} name={state.garant.name}/><br />
                    </Card.Body>
                </Card>
            </Col>
        </Row>
        <Row>
            <Col>
                <TimeTableMedium type='subject' id={props.id}/>
            </Col>
        </Row>
        </>
    )
}

export const SubjectPage = (props) => {
    const { id } = useParams();
    const name = 'fetched name'
    return (
        <SubjectLarge id={id} name={name} />
    )
}