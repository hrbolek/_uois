import {
    Link,
    useParams
  } from "react-router-dom";

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

import { TeacherSmall } from '../teacher/teacher';
import { StudentSmall } from '../student/student';

import { root } from '../index'

const groupRoot = root + '/groups'

export const GroupSmall = (props) => {
    //embeded Student
    return (
        <Link to={groupRoot + `/${props.id}`}>{props.name}</Link>
    )
}

export const GroupMedium = (props) => {
    return (
        <Card>
            {/*<Card.Img variant="top" src="holder.js/100px180" />*/}
            <Card.Body>
                <Card.Title>Skupina ID:{props.id}, {props.name}</Card.Title>
                <Card.Text>
                </Card.Text>
                <Button variant="primary">Go somewhere</Button>
            </Card.Body>
        </Card>            
    )
}

export const GroupLarge = (props) => {
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
                        <a href={'mailto:student1@unob.cz?cc=student2@unob.cz;student3@unob.cz&subject=Email z IS'}>@</a>
                    </Card.Body>
                </Card>
            </Col>
        </Row>
        <Row>
            <Col>
                <Card>
                    <Card.Header className='bg-success bg-gradient text-white'>
                        <Card.Title>Studenti:</Card.Title>
                    </Card.Header>
                    <Card.Body>
                        <StudentSmall id='1587' name='Novák' /><br />
                        <StudentSmall id='1774' name='Rozbilová' /><br />
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

export const GroupPage = (props) => {
    const { id } = useParams();
    const name = 'fetched name'
    return (
        <GroupLarge id={id} name={name} />
    )
}

export const GroupList = (props) => {
    return (
        <div>Toto je seznam skupin</div>
    )
}