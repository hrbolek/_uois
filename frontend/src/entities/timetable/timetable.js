import Container from 'react-bootstrap/Container';
import {
    Link,
    useParams, useLocation, useNavigate 
  } from "react-router-dom";

import React, { useState, useEffect } from 'react';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

import SVG from 'react-inlinesvg';

import { root } from '../index'

/** @module TimeTable */

const timetableRoot = root + '/timetable'

export const TimeTableSmall = (props) => {
    return (
        <Link to={timetableRoot + `/${props.id}`}>Rozvrh ({props.id})</Link>
    )
}

//<SVG src={props.link} width={'700'} height={'300'} viewBox='10 40 1370 500' />
//<Card.Title>Rozvrh <Link to={`${root}/svg/${props.type}/${props.id}/?start=2021-11-10`}> velký </Link> (<Link to={`${root}/A4/${props.type}/${props.id}/`}> A4 </Link> )</Card.Title>
//<SVG src={`/svg/${props.type}/${props.id}/?start=2021-11-10`} width={'100%'} height={'100%'} viewBox='10 20 1400 550' />
export const TimeTableMedium = (props) => {
    
    return (
        <Card>
            <Card.Header>
                <Card.Title>Rozvrh <Link to={`${root}/svg/${props.type}/${props.id}/`}> velký </Link> (<Link to={`${root}/A4/${props.type}/${props.id}/`}> A4 </Link> )</Card.Title>
            </Card.Header>
            <Card.Body>
                <div>
                <SVG src={`/svg/${props.type}/${props.id}/?start=2021-11-08`} width={'100%'} height={'100%'} viewBox='10 20 1400 550' />
                </div>
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

//<TimeTableFull id={id} />
export const TimeTablePage = (props) => {
    const { id, entity } = useParams();
    const { search, location } = useLocation();
    const navigate = useNavigate();
    //let start = (new Date()) + '';
    const start = (new URLSearchParams(search)).get('start') || (new Date().toISOString().substring(0, 10));
    //if (props.)
    const PrevWeekClick = () => {
        let parsed = start.split('-')
        //console.log(JSON.stringify(parsed))
        let nextDate = new Date(parsed[0], parsed[1] - 1, parsed[2], 12) //MONTH Index WTF https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/Date
        //console.log(JSON.stringify(nextDate))
        nextDate.setDate(nextDate.getDate() - 7);
        //console.log(JSON.stringify(nextDate)) //http://localhost:3000/ui/svg/teacher/633/?start=2021-10-07
        navigate(`./?start=${nextDate. toISOString().substring(0, 10)}`)//, {replace: true})
    }
    const NextWeekClick = () => {
        let parsed = start.split('-')
        //console.log(JSON.stringify(parsed))
        let nextDate = new Date(parsed[0], parsed[1] - 1, parsed[2], 12) //MONTH Index WTF https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/Date
        //console.log(JSON.stringify(nextDate))
        nextDate.setDate(nextDate.getDate() + 7);
        //console.log(JSON.stringify(nextDate)) //http://localhost:3000/ui/svg/teacher/633/?start=2021-10-07
        navigate(`./?start=${nextDate.toISOString().substring(0, 10)}`)//, {replace: true})
    }

     return (
        <>
            <object id="svg1" data={`/svg/${entity}/${id}/?start=${start}`} type="image/svg+xml"></object>
            <br/>
            <Row>
                <Col></Col>
                <Col>
                    <div className="d-grid gap-2">
                        <Button variant="outline-primary" onClick={PrevWeekClick}>Předcházející týden</Button>
                    </div>
                </Col>
                <Col>
                    <div className="d-grid gap-2">
                        <Button variant="outline-success"> {id}</Button>
                    </div>                
                </Col>
                <Col>
                    <div className="d-grid gap-2">
                        <Button variant="outline-primary" onClick={NextWeekClick}>Následující týden</Button>
                    </div>
                </Col>
                <Col></Col>
            </Row>
        </>
    )

    /*
    return (
        <div>
            <SVG src={`/svg/nav/${entity}/${id}/`} width={'100%'} height={'100%'} viewBox='10 20 1400 550' />
        </div>
    ) */

}

/**
 * Renders a page representing a time table sheet, designed as a component for a ReactJS router
 * @param {*} props - extra props for encapsulated components / visualisers
 * @function
 */
export const TimeTableA4Page = (props) => {
    const { id, entity } = useParams();
    const { search, location } = useLocation();

     return (
        <>
            <object id="svg1" data={`/svg/A4/`} type="image/svg+xml"></object>
        </>
    )

    /*
    return (
        <div>
            <SVG src={`/svg/nav/${entity}/${id}/`} width={'100%'} height={'100%'} viewBox='10 20 1400 550' />
        </div>
    ) */

}