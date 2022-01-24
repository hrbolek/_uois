import { Link, useParams } from "react-router-dom";

import Card from 'react-bootstrap/Card';
import { Row } from "react-bootstrap";
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

export function StudentSmall(props) {
    return (
        <Link to={root + "/users/student/" + (props.id)}>{props.name} {props.surname}</Link>
    )
}

export function StudentMedium(props) {
    let faculties = props.faculty.map((item) => (<FacultySmall key={item.id} {...item} />))
    let groups = props.groups.map((item) => (<GroupSmall key={item.id} {...item} />))

    return (
        <div className="card mb-3">
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
        </div>
    )
}

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

function SeznamPredmetuUStudenta(props) {
    let subjects = props.subjects.map((subject, index) => (<li><SubjectSmall {...subject} /> </li>))

    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Předměty</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul>
                    {subjects}
                </ul>
            </Card.Body>
        </div>
    )
}

export function StudentLarge(props) {

    return (
        <div className="card">
            <div className="card-header mb-3">
                <h4>Karta studenta</h4>
            </div>

            <div className="col">
                <Row>
                    <div className="col-3">
                        <StudentMedium {...props} />
                        <ContactInfo {...props} />
                    </div>
                    <div className="col-6">
                        <RozvrhMedium />
                    </div>
                    <div className="col-3">
                        <StudentProgram {...props} /> <br />
                        <SeznamPredmetuUStudenta {...props} />
                        
                    </div>
                </Row>
            </div>
        </div>
    )
}

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

  
export const StudentLargeFetching = (props) => {

    const Visualizer = props.as || StudentLargeStoryBook;
    const queryFunc = props.with || StudentLargeQuery;

    const [state, error] = useQueryGQL(props.id, queryFunc, (response) => response.data.user, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <Visualizer {...state} />
    } else {
        return <Loading>Uživatel {props.id}</Loading>
    }
}

export const StudentPage = (props) => {
    const { id } = useParams();

    return (
        <StudentLargeFetching {...props} id={id} as={StudentLargeStoryBook}/>
    )    
}
//ContactInfo
/*
export function StudentPage(props) {
    const [state, setState] = useState(
        {
            'id': props.id,
            'name': props.name,
            'lastname': props.lastname,
            'degreeRank': 'ing. por.',
            'grade': '3',
            "email": props.name.toLowerCase() + '.' + props.lastname.toLowerCase() + '@unob.cz',
            'phone': '720 525 980',
            'areal': 'Kasárny Černá Pole',
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
    )

    useEffect(() => {
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
                    user(id: ${props.id}) {
                      id
                      name
                      surname
                      email
                      groups: groupsByType(typeId: 1) {
                        id
                        name
                      }
                      faculty: groupsByType(typeId: 2) {
                        id
                        name
                      }
                      subjects: groupsByType(typeId: 0) {
                        id
                        name
                      }
                    }
                  }
                `
            }),
        })
            .then(response => response.json())
            .then(data => setState(data.data))
            .then(() => console.log('data logged'))
            .catch(error => console.log('error nacteni'))
    }, [props.id])

    // const groups = []
    // for(index = 0; index < state.groups.length; index++) {
    //     if(index>0) groups.push(', ')
    //     const sgItem = state.groups[index]
    //     groups.push(<GroupS {...props} id={sgItem.id} name={sgItem.name} key={sgItem.id}/>);
    // }

    return (
        <StudentLarge {...state} {...props} />
    )
}
*/
function RozvrhMedium() {
    return ( 
        <TimeTableMedium type={'student'} id={1} />
    )
}

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

