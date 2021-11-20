import Container from 'react-bootstrap/Container';
import {
    Link,
    useParams
  } from "react-router-dom";
import { useEffect, useState } from "react";

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Table from 'react-bootstrap/Table';

import { root } from '../index'

import { GroupSmall } from '../group/group';

const teacherRoot = root + '/teachers'

export const TeacherSmall = (props) => {
    return (
        <Link to={teacherRoot + `/${props.id}`}>{props.name}</Link>
    )
}

export const TeacherMedium = (props) => {
    return (
        <div>Učitel podrobněji</div>
    )
}

export const TeacherLarge = (props) => {
    const [state, setState] = useState(
        {
            'id': props.id,
            'name': props.name,
            'faculty': 'FVT',
            'department': 'K209',
            'subjects': [
                {'id': 458, 'name': 'subj1'}
            ]
        })

    useEffect(()=>{

    })
    return (
        <>
            <Row>
                <Col>
                    <Card>
                        <Card.Header className='bg-success bg-gradient text-white'>
                            <Card.Title>Základní informace</Card.Title>
                        </Card.Header>
                        <Card.Body>
                            <Table striped bordered hover>
                            <colgroup>
                                <col className="col-md-3" />
                                <col className="col-md-9" />
                            </colgroup>                                
                            <tbody>
                                <tr><td><b>Akademický pracovník ({state.id})</b></td><td>{state.name}</td></tr>
                                <tr><td><b>Fakulta</b> </td><td>{state.faculty}</td></tr>
                                <tr><td><b>Katedra</b> </td><td>{state.department}</td></tr>
                            </tbody>
                        </Table>

                        </Card.Body>
                    </Card>
                </Col>
            </Row>
            <Row>
                <Col>
                    <Card>
                        <Card.Header className='bg-success bg-gradient text-white'>
                            <Card.Title>Vyučované předměty</Card.Title>
                        </Card.Header>
                        <Card.Body>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
            <Row>
                <Col>
                    <Card>
                        <Card.Header className='bg-success bg-gradient text-white'>
                            <Card.Title>Garance</Card.Title>
                        </Card.Header>
                        <Card.Body>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
            <Row>
                <Col>
                    <Card>
                        <Card.Header className='bg-success bg-gradient text-white'>
                            <Card.Title>Vyučované skupiny</Card.Title>
                        </Card.Header>
                        <Card.Body>
                            <GroupSmall id={758} name={'23-5KB'} /> <br />
                            <GroupSmall id={862} name={'22-5ASV'} />
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </>
    )
}

export const TeacherPage = (props) => {
    const { id } = useParams();
    const name = 'Alexandr Štefek'
    return (
        <TeacherLarge id={id} name={name} />
    )
}