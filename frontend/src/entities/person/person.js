import { Link } from "react-router-dom";

import Card from 'react-bootstrap/Card';
import { Col, Row } from "react-bootstrap";


import { root } from '../index';


export function PersonSmall(props) {
    return (
        <Link to={root + "/users/" + (props.id + 1)}>{props.name} {props.lastname}</Link>
    )
}

export function PersonMedium(props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title><PersonSmall {...props} /></Card.Title>
            </Card.Header>
            <Card.Body>
                <Card.Text>
                    Jmeno: {props.name} Prijmeni: {props.lastname}<br/>
                    Titul: {props.degreeRank ? props.degreeRank : 'Mgr. npor.'} <br/>
                    Rocnik: {props.grade ? props.grade : '3.'} Skupina: {props.group ? props.group : '21-5KB'}<br/>
                    E-mail: Telefon:
                </Card.Text>
            </Card.Body>
        </Card>
    )
}

export function PersonLarge(props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title>Karta uživatele</Card.Title>
            </Card.Header>
            <Row>
                <div><br/></div>
            </Row>
            <Row>
                <Col>
                    <PersonMedium {...props}/>
                </Col>
            </Row>
        </Card>
    )
}
