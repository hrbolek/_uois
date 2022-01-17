import { Link, useParams } from "react-router-dom";

import Card from 'react-bootstrap/Card';
import { Row } from "react-bootstrap";
import { useEffect, useState } from "react";

import image from '../rozvrhSnimek.png'
import { DepartmentSmall } from "../group/department";


import { root } from '../index';
import { useQueryGQL, Loading, LoadingError } from "../index";

export function TeacherSmall(props) {
    return (
        <Link to={root + "/users/teacher/" + (props.id)}>{props.name} {props.surname}</Link>
    )
}

export function TeacherMedium(props) {
    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Vyučující - <TeacherSmall {...props} /></Card.Title>
            </Card.Header>
            <Card.Body>
                <Card.Text>
                    <b>Jméno příjmení:</b> {props.name} {props.surname}<br />
                    <b>Titul:</b> {props.degreeRank}<br />
                    <b>Katedra:</b> {props.departments}<br />
                    {/*<b>Fakulta:</b> {props.faculty}*/}
                </Card.Text>
            </Card.Body>
        </div>
    )
}

export function TeacherLarge(props) {
    let subjects = props.subjects.map((item) => (<li key={item.id}><Link key={item.id} to={'404'}>{item.name}</Link></li>))

    const departments = []
    for (var index = 0; index < props.departments.length; index++) {
        if (index > 0) {
            departments.push(', ');
        }
        const sgItem = props.departments[index]
        departments.push(<DepartmentSmall {...props} id={sgItem.id} name={sgItem.name} key={sgItem.id} />);
    }

    return (
        <div className="card w-75">
            <div className="card-header mb-3">
                <h4>Karta uživatele</h4>
            </div>
            <div className="col">
                <Row>
                    <div className="col-3">
                        <TeacherMedium {...props} departments={departments} />
                        <ContactInfo {...props} />
                    </div>
                    <div className="col-6">
                        <RozvrhMedium />
                    </div>
                    <div className="col-3">
                        <SeznamPredmetu subjects={subjects} />
                    </div>
                </Row>
            </div>
        </div>
    )
}
/*
export function TeacherPage(props) {
    const [state, setState] = useState(
        {
            'id': props.id,
            'name': props.name,
            'lastname': props.lastname,
            'degreeRank': 'ing. plk.',
            "email": props.name.toLowerCase() + '.' + props.lastname.toLowerCase() + '1@unob.cz',
            'phone': '973 274 160',
            'areal': 'Kasárny Šumavská',
            'building': '5',
            'room': '104',
            'faculty': [
                { 'id': 23, 'name': 'FVT' }
            ],
            'departments': [
                { 'id': 1, 'name': 'K-209' },
                { 'id': 2, 'name': 'K-207' }
            ],
            'subjects': [
                { 'id': 25, 'name': 'Informatika' },
                { 'id': 1, 'name': 'Analýza informačních zdrojů' },
                { 'id': 4, 'name': 'Kybernetická bezpečnost' },
                { 'id': 5, 'name': 'Počítačové sítě a jejich bezpečnost' }
            ]
        }
    )

    console.log(state)

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
                        lastname
                        degreeRank
                        email
                        phone
                        areal
                        building
                        room
                        faculty: groupsByType(type: 0) {
                            id
                            name
                        }
                        departments: groupsByType(type: 1) {
                            id
                            name
                        }
                        subjects: groupsByType(type: 2) {
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


    return (
        <TeacherLarge {...props} {...state} />
    )
}
*/

export const TeacherLargeQuery = (id) => 
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
                user(id: ${id}) {
                    id
                    name
                    surname
                    email
    
                    faculty: groupsByType(typeId: 0) {
                        id
                        name
                    }
                    departments: groupsByType(typeId: 1) {
                        id
                        name
                    }
                    subjects: groupsByType(typeId: 2) {
                        id
                        name
                    }
                }
            }
            `
        }),
    })

export const TeacherLargeStoryBook = (props) => {
    const extendedProps = {
        'id': props.id,
        'name': 'props.name',
        'lastname': 'props.lastname',
        'degreeRank': 'ing. plk.',
        "email": 'props.name.toLowerCase()' + '.' + 'props.lastname.toLowerCase()' + '1@unob.cz',
        'phone': '973 274 160',
        'areal': 'Kasárny Šumavská',
        'building': '5',
        'room': '104',
        'faculty': [
            { 'id': 23, 'name': 'FVT' }
        ],
        'departments': [
            { 'id': 1, 'name': 'K-209' },
            { 'id': 2, 'name': 'K-207' }
        ],
        'subjects': [
            { 'id': 25, 'name': 'Informatika' },
            { 'id': 1, 'name': 'Analýza informačních zdrojů' },
            { 'id': 4, 'name': 'Kybernetická bezpečnost' },
            { 'id': 5, 'name': 'Počítačové sítě a jejich bezpečnost' }
        ]
    }
    return <TeacherLarge {...extendedProps} {...props} />;
}

export const TeacherLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, TeacherLargeQuery, (response) => response.data.user, [props.id])
    
    if (state != null) {
        return <TeacherLargeStoryBook {...state} />
    } else if (error != null) {
        return <LoadingError error={error} />
    } else {
        return <Loading>Uživatel {props.id}</Loading>
    }
}

export const TeacherPage = (props) => {
    const { id } = useParams();

    return (
        <TeacherLargeFetching {...props} id={id} />
    )    
}



function RozvrhMedium() {
    return (
        <Card>
            <Card.Header>
                <Card.Title>Rozvrh tento týden</Card.Title>
            </Card.Header>
            <Card.Body>
                <img src={image} alt="Rozvrh" width={'100%'} />
            </Card.Body>
        </Card>
    )
}

function ContactInfo(props) {
    //data=props.datas;
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
            </Card.Body>
        </div>
    )
}

function SeznamPredmetu(props) {
    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Předměty</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul>
                    {props.subjects}
                </ul>
            </Card.Body>
        </div>
    )
}