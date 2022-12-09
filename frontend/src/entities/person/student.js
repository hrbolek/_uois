import { Link, useParams } from "react-router-dom";

import Card from 'react-bootstrap/Card';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { useEffect, useState } from "react";

import image from '../rozvrhSnimek.png'
import { GroupSmall } from "../group/group";
import { FacultySmall } from "../group/faculty";
import { TeacherSmall } from "./teacher";

import { root } from '../index';
import { useQueryGQL, Loading, LoadingError } from "../index";
import { TimeTableMedium } from "../timetable/timetable";
import { SubjectSmall } from "../studyprogram/subject";
import { ProgramSmall } from '../studyprogram/studyprogram';


/** @module Student */

/**
 * Renders a link to a student's page
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {string} props.name - Student's name
 * @function
 */
export function StudentSmall(props) {
    return (
        <Link to={root + "/users/student/" + (props.id)}>{props.name} {props.surname}</Link>
    )
}

/**
 * Renders a medium set of student's data, it is compatible with {@link StudentLarge}
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {string} props.name - Student's name
 * @param {*} props.faculty - Student's faculty
 * @param {*} props.groups - Student's groups
 * @function
 */
export function StudentMedium(props) {
    let faculties = props.faculty.map((item, index) => index === 0 ? (<FacultySmall key={item.id} {...item} />) : (<>, <FacultySmall key={item.id} {...item} /></>))
    let groups = props.groups.map((item, index) => index === 0? (<GroupSmall key={item.id} {...item} />) : (<>, <GroupSmall key={item.id} {...item} /></>))

    return (
        <Card>
            <Card.Header>
                <Card.Title>Student - <StudentSmall {...props.person} /></Card.Title>
            </Card.Header>
            <Card.Body>
    
                <Card.Text>
                    <b>Jméno  příjmení:</b> {props.person.name} {props.person.surname}<br />
                    <b>Titul:</b> {props.degreeRank} <b>Ročník:</b> {props.grade} <br />
                    <b>Skupina:</b> {groups}<br />
                    <b>Fakulta:</b> {faculties}
                </Card.Text>
            </Card.Body>
        </Card>
    )
}

/**
 * Renders a program student is studying
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {*} props.program - the program
 * @function
 */
export const StudentProgram = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>Program</Card.Title>
            </Card.Header>
            <Card.Body>
                <ProgramSmall {...props.program} />
            </Card.Body>
        </Card>
        
    )
}

/**
 * Renders a student's subject list
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {*} props.subjects - identification
 * @function
 */
function SeznamPredmetuUStudenta(props) {
    let subjects = props.subjects.map((subject, index) => (<li><SubjectSmall {...subject} /> </li>))

    return (
        <Card>
            <Card.Header>
                <Card.Title>Předměty</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul>
                    {subjects}
                </ul>
            </Card.Body>
        </Card>
    )
}


/**
 * Renders a student's timetable
 * @param {*} props 
 * @param {*} props.id - identification
 * @function
 */
function RozvrhMedium(props) {
    return ( 
        <TimeTableMedium type={'student'} id={props.id} />
    )
}

/**
 * Renders a page with data representing a student contacts
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {*} props.email - student's email
 * @param {string} props.name - Student's name
 * @function
 */
 function ContactInfo(props) {
    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Kontaktní údaje</Card.Title>
            </Card.Header>
            <Card.Body>
                <b>E-mail:</b> {props.email}<br />
                <b>Telefon:</b> {props.phone ? props.phone : 'Neuvedeno'}<br />
                <b>Areál: </b> {props.areal}<br />
                <b>Budova: </b>{props.building} <b>Místnost:</b> {props.room}<br />
                <hr />
                <b>Velitel roty:</b> <TeacherSmall id={23} name='Stanislav' surname='Dobrušák' /><br />
                <b>Velitel čety:</b> <StudentSmall id={28} name='Pavel' surname='Rajská' /><br />
                <b>Vedoucí katedry:</b> <TeacherSmall id={21} name='František' surname='Petr' /><br />
            </Card.Body>
        </div>
    )
    // <b>Velitel roty:</b> <PersonS id={23} name='Stanislav' lastname='Dobrušák' appRoot={props.appRoot}/><br />
    // <b>Velitel čety:</b> <PersonS id={28} name='Pavel' lastname='Rajská' appRoot={props.appRoot}/><br />
    // <b>Vedoucí katedry:</b> <PersonS id={21} name='František' lastname='Petr' appRoot={props.appRoot}/><br />

}

/**
 * Renders a page with data representing a student
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {*} props.person - peronification fo student
 * @function
 */
 export function StudentLarge(props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Karta studenta
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={3}>
                        <StudentMedium {...props} /><br />
                        <ContactInfo {...props} />
                    </Col>
                    <Col md={6}>
                        <RozvrhMedium {...props}/>
                    </Col>
                    <Col md={3}>
                        <StudentProgram {...props} /> <br />
                        <SeznamPredmetuUStudenta {...props} />
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}

/**
 * Renders a page with data representing a student
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {*} props.person - peronification fo student
 * @param {string} props.name - Student's name
 * @function
 */
export const StudentLargeStoryBook = (props) => {
    const extendedProps = {
        'id': 1,
        'person': {
            'id': 1,
            'name': 'Name',
            'surname': 'Lastname',
            "email": 'name.lastname@unob.cz',   
        },
        'degreeRank': 'ing. por.',
        'grade': '3',
        'phone': '799 999 999',
        'areal': 'Kasárna Černá Pole',
        'building': '3',
        'room': '422',
        'VR': 'def',
        'VC': 'def',
        'VK': 'def',
        'faculty': [
            { 'id': 23, 'name': 'FVT' }
        ],
        'groups': [
            { 'id': 21, 'name': '23-5KB' },
            { 'id': 22, 'name': '24-5KB' }
        ],
        'subjects': [
            { 'id': 25, 'name': 'Informatika' },
            { 'id': 1, 'name': 'Analýza informačních zdrojů' },
            { 'id': 3, 'name': 'Anglický jazyk' },
            { 'id': 2, 'name': 'Tělesná výchova' },
            { 'id': 4, 'name': 'Kybernetická bezpečnost' },
            { 'id': 5, 'name': 'Počítačové sítě a jejich bezpečnost' }
        ]
    }

    return <StudentLarge {...extendedProps} {...props} />;
}

/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
export const StudentLargeQuery = (id) => 
    fetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `
                query {
                    user: student(id: ${id}) {
                      id
                      person {
                        id
                        name
                        surname
                        email
                      }
                      program {
                        id
                        name
                        subjects {
                          id
                          name
                        }
                      }
                    }
                  }
            `

        }),
    })

/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
export const StudentMediumQuery = (id) => 
    fetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `
                query {
                    user: student(id: ${id}) {
                        id
                        person {
                            id
                            name
                            surname
                            email
                        }
                    }
                }
            `
        }),
    })

  
/**
 * Fetch the data from API endpoint and renders a page representing a student
 * @param {*} props - extra props for encapsulated components / visualisers
 * @param {*} [props.as = StudentLargeStoryBook] - ReactJS component (function) which is responsible for rendering
 * @param {*} [props.with = StudentLargeQuery] - function fetching the data and returning promise with the data from API endpoint
 * @function
 */
export const StudentLargeFetching = (props) => {

    const Visualizer = props.as || StudentLargeStoryBook;
    const queryFunc = props.with || StudentLargeQuery;

    const [state, error] = useQueryGQL(props.id, queryFunc, (response) => response.data.user, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <Visualizer {...props} {...state} />
    } else {
        return <Loading>Uživatel {props.id}</Loading>
    }
}

/**
 * Renders a page representing a student, designed as a component for a ReactJS router
 * @param {*} props - extra props for encapsulated components / visualisers
 * @function
 */
export const StudentPage = (props) => {
    const { id } = useParams();

    return (
        <StudentLargeFetching {...props} id={id} as={StudentLargeStoryBook}/>
    )    
}