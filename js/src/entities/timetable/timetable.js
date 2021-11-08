import Container from 'react-bootstrap/Container';
import {
    Link,
    useParams
  } from "react-router-dom";

import React, { useState, useEffect } from 'react';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';

import SVG from 'react-inlinesvg';

import { root } from '../index'

const timetableRoot = root + '/timetable'

export const TimeTableSmall = (props) => {
    return (
        <Link to={timetableRoot + `/${props.id}`}>Rozvrh ({props.id})</Link>
    )
}

export const TimeTableMedium = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>Rozvrh ({props.type} / {props.id})</Card.Title>
            </Card.Header>
            <Card.Body>
                <SVG src={'https://upload.wikimedia.org/wikipedia/commons/1/15/Svg.svg'} width={'100%'} height="auto" />

            </Card.Body>
        </Card>
    )
}

export const TimeTableFull = (props) => {
    return (
        <Row>
            <Col>
                <TimeTableMedium {...props} />
            </Col>
        </Row>
    )
}

export const TimeTablePage = (props) => {
    const { id } = useParams();
    return (
        <TimeTableFull id={id} />
    )

}