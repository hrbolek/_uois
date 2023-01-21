import { Link, useParams } from "react-router-dom";

import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import { useEffect, useState } from "react";

import image from '../rozvrhSnimek.png';
import { StudentSmall } from "../person/student";
import { DepartmentSmall } from "../group/department";
import { TeacherSmall } from "../person/teacher";
import { TimeTableMedium } from '../timetable/timetable';

import { root } from '../index';
import { useQueryGQL, Loading, LoadingError } from "../index";
import { SubjectSmall } from "../studyprogram/subject";
import { ProgramSmall } from "../studyprogram/studyprogram";

/** @module Group */

export function GroupSmall(props) {
    return (
        <Link to={root + "/groups/group/" + props.id}>{props.name}</Link>
    )
}

export function GroupMedium(props) {
    const faculties = []
    for (var index = 0; index < props.faculty.length; index++) {
        if (index > 0) faculties.push(', ')
        const sgItem = props.faculty[index]
        faculties.push(<DepartmentSmall {...props} id={sgItem.id} name={sgItem.name} key={sgItem.id} />);
    }

    return (
        <Card>
            <Card.Header>
                <Card.Title>Skupina <b><GroupSmall {...props} /></b></Card.Title>
            </Card.Header>
            <Card.Body>
                <b>Fakulta:</b> {faculties} <br />
                <b>Ročník:</b> {props.grade} <br />
                <b>Program:</b> <ProgramSmall id={1} name={'Kybernetická bezpečnost'} />
            </Card.Body>
        </Card>
    )
}


/*
export function GroupPage(props) {
    const [state, setState] = useState(
        {
            'id': props.id,
            'name': props.name,
            'grade': '3',
            'specialization': 'Kybernetická bezpečnost',
            'VR': 'def',
            'VC': 'def',
            'VK': 'def',
            'faculty': [
                { 'id': 23, 'name': 'FVT' }
            ],
            'subjects': [
                { 'id': 25, 'name': 'Informatika' },
                { 'id': 1, 'name': 'Analýza informačních zdrojů' },
                { 'id': 3, 'name': 'Anglický jazyk' },
                { 'id': 2, 'name': 'Tělesná výchova' },
                { 'id': 4, 'name': 'Kybernetická bezpečnost' },
                { 'id': 5, 'name': 'Počítačové sítě a jejich bezpečnost' }
            ],
            'students': [
                { 'id': 1, 'name': 'Honza Bernard' },
                { 'id': 2, 'name': 'Pavel Motol' },
                { 'id': 3, 'name': 'Dominik Vaněk' },
                { 'id': 4, 'name': 'Andrea Svobodova' },
                { 'id': 5, 'name': 'Michal Mrkev' },
                { 'id': 6, 'name': 'Patrik Němý' },
                { 'id': 7, 'name': 'Jiřina Stará' },
                { 'id': 8, 'name': 'Petr Filip' },
                { 'id': 9, 'name': 'Jiří Grau' },
                { 'id': 10, 'name': 'Teodor Velký' },
                { 'id': 11, 'name': 'Alexandr Veliký' },
                { 'id': 22, 'name': 'Aleš Máchal' }
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
                        VR
                        VC
                        faculty: groupsByType(type: 0) {
                            id
                            name
                        }
                        groups: groupsByType(type: 1) {
                            id
                            name
                        }
                        subjects: groupsByType(type: 2) {
                            id
                            name
                        }
                        students: groupsByType(type: 3) {
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
        <GroupLarge {...state} {...props} />
    )
}
*/

// function RozvrhMedium() {
//     return (
//         <Card>
//             <Card.Header>
//                 <Card.Title>Týdenní rozrvh</Card.Title>
//             </Card.Header>
//             <Card.Body>
//                 <img src={image} alt="Rozvrh" width={'100%'} />
//             </Card.Body>
//         </Card>
//     )
// }


function RozvrhMedium(props) {
    return (
        <TimeTableMedium type={'student'} id={props.id} />
    )
}

function SeznamPredmetu(props) {
    let subjects = props.subjects.map((subject, index) => (<li key={index}><SubjectSmall {...subject}/></li>))

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

function SeznamStudentu(props) {
    let students = props.students.map((item) => (<li key={item.id}><StudentSmall key={item.id} {...item} appRoot={props.appRoot} /></li>))
    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Studenti</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul>
                    {students}
                </ul>
            </Card.Body>
        </div>
    )
}

function ContactInfo(props) {
    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Nadřízení</Card.Title>
            </Card.Header>
            <Card.Body>
                <b>Velitel roty:</b> <TeacherSmall id={23} name='Stanislav' surname='Dobrušák'  /><br />
                <b>Velitel čety:</b> <StudentSmall id={28} name='Pavel' surname='Rajská'  /><br />
                <b>Vedoucí katedry:</b> <TeacherSmall id={21} name='František' surname='Novák' /><br />
            </Card.Body>
        </div>
    )
}

export function GroupLarge(props) {

    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Karta učební skupiny
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={3}>
                        <GroupMedium {...props} /> <br/>
                        <ContactInfo {...props} />

                    </Col>
                    <Col md={2}>
                        <SeznamStudentu {...props} />
                    </Col>
                    <Col md={5}>
                        <RozvrhMedium {...props}/>
                    </Col>
                    <Col md={2}>
                        <SeznamPredmetu {...props} />
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}

/**
 * Renders a page with data representing a group, contains predefined data which can are overrided by props
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {string} props.name - name
 * @function
 */
export const GroupLargeStoryBook = (props) => {
    const extraProps = {
        'id': props.id,
        'name': props.name,
        'grade': '3',
        'specialization': 'Kybernetická bezpečnost',
        'VR': 'def',
        'VC': 'def',
        'VK': 'def',
        'faculty': [
            { 'id': 23, 'name': 'FVT' }
        ],
        'subjects': [
            { 'id': 25, 'name': 'Informatika' },
            { 'id': 1, 'name': 'Analýza informačních zdrojů' },
            { 'id': 3, 'name': 'Anglický jazyk' },
            { 'id': 2, 'name': 'Tělesná výchova' },
            { 'id': 4, 'name': 'Kybernetická bezpečnost' },
            { 'id': 5, 'name': 'Počítačové sítě a jejich bezpečnost' }
        ],
        'students': [
            { 'id': 1, 'name': 'Honza Bernard' },
            { 'id': 2, 'name': 'Pavel Motol' },
            { 'id': 3, 'name': 'Dominik Vaněk' },
            { 'id': 4, 'name': 'Andrea Svobodova' },
            { 'id': 5, 'name': 'Michal Mrkev' },
            { 'id': 6, 'name': 'Patrik Němý' },
            { 'id': 7, 'name': 'Jiřina Stará' },
            { 'id': 8, 'name': 'Petr Filip' },
            { 'id': 9, 'name': 'Jiří Grau' },
            { 'id': 10, 'name': 'Teodor Velký' },
            { 'id': 11, 'name': 'Alexandr Veliký' },
            { 'id': 22, 'name': 'Aleš Máchal' }
        ]
    }


    return <GroupLarge {...extraProps} {...props} />
}

/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
export const GroupLargeQuery = (id) => 
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
                group(id: ${id}) {
                    id
                    name
                    members {
                      id
                      name
                      surname
                      address
                      email
                    }
                  }
            }
            `
        }),
    })

/**
 * Fetch the data from API endpoint and renders a page representing a group
 * @param {*} props - extra props for encapsulated components / visualisers
 * @param {*} [props.as = GroupLargeStoryBook] - ReactJS component (function) which is responsible for rendering
 * @param {*} [props.with = GroupLargeQuery] - function fetching the data and returning promise with the data from API endpoint
 * @function
 */
export const GroupLargeFetching = (props) => {

    const Visualizer = props.as || GroupLargeStoryBook;
    const queryFunc = props.with || GroupLargeQuery;

    const [state, error] = useQueryGQL(props.id, queryFunc, (response) => response.data.group, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <Visualizer {...props} {...state} />
    } else {
        return <Loading>Skupina {props.id}</Loading>
    }
}

export const GroupPage = (props) => {
    const { id } = useParams();

    return (
        <GroupLargeFetching {...props} id={id} />
    )       
}