import Container from 'react-bootstrap/Container';
import {
    Link,
    useParams
  } from "react-router-dom";

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

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
    return (
        <>
            <Row>
                <Col>
                    <Card>
                        <Card.Header>
                            <Card.Title>Základní informace</Card.Title>
                        </Card.Header>
                        <Card.Body>
                            {props.id}<br />
                            {props.name}
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
            <Row>
                <Col>
                    <Card>
                        <Card.Header>
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
                        <Card.Header>
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
                        <Card.Header>
                            <Card.Title>Vyučované skupiny</Card.Title>
                        </Card.Header>
                        <Card.Body>
                            <GroupSmall id={758} name={'23-5KB'} />
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
    const name = 'fetched name'
    return (
        <TeacherLarge id={id} name={name} />
    )
}