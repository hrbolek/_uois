import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import { Card } from "react-bootstrap";
import { TeacherSmall } from "../person/teacher";
import { FacultySmall } from "./faculty";

import { root } from '../index';
import { useQueryGQL, Loading, LoadingError } from "../index";

export function DepartmentSmall(props) {
    return (
        <Link to={root + "/groups/department/" + props.id}>{props.name}</Link>
    )
}

export function DepartmentMedium(props) {
    return (
        <Card className='mb-3'>
            <Card.Header>
                <Card.Title>Katedra <b><DepartmentSmall {...props} /></b></Card.Title>
            </Card.Header>
            <Card.Body>
                <b>Název:</b> {props.fullname}<br />
                <b>Vedoucí katedry:</b> {props.VK}<br />
                <b>Fakulta:</b> <FacultySmall {...props} name={props.FacultyName} id={props.id}/><br />
            </Card.Body>
        </Card>
    )
}

export function DepartmentLarge(props) {
    let teachers = props.teachers.map((item) => (<li key={item.id}><TeacherSmall key={item.id} {...item} /></li>))

    return (
        <div className="card w-50">
            <div className="card-header mb-3">
                <h4>Karta katedry</h4>
            </div>
            <div className='col'>
                <div className='row'>
                    <div className='col'>
                        <DepartmentMedium {...props} FacultyName={props.faculty[0].name} id={props.faculty[0].id} />
                        <ContactInfo {...props} />
                    </div>
                    <div className='col'>
                        <SeznamUcitelu teachers={teachers} />
                    </div>
                </div>
            </div>
        </div>
    )
}

export const DepartmentLargeStoryBook = (props) => {
    const extendedProps = {
        'id': props.id,
        'name': props.name,
        'fullname': 'Katedra informatiky a kybernetických operací',
        'areal': 'Kasárny Šumavská',
        'building': '3',
        'faculty': [
            { 'id': 23, 'name': 'FVT' }
        ],
        'teachers': [
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

    return <DepartmentLarge {...extendedProps} {...props} />;
}

export const DepartmentLargeQuery = (id) => 
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
                    grouptypeId
                    roles {
                      user {
                        id
                        name
                        surname
                        email
                      }
                      
                      roletype {
                        id
                        name
                      }
                    }
                    teachers: users {
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

export const DepartmentLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, DepartmentLargeQuery, (response) => response.data.group, [props.id])
    
    if (state != null) {
        return <DepartmentLargeStoryBook {...state} />
    } else if (error != null) {
        return <LoadingError error={error} />
    } else {
        return <Loading>Uživatel {props.id}</Loading>
    }
}

export const DepartmentPage = (props) => {
    const { id } = useParams();

    return (
        <DepartmentLargeFetching {...props} id={id} />
    )       
}
/*
export function DepartmentPage(props) {
    const [state, setState] = useState(
        {
            'id': props.id,
            'name': props.name,
            'fullname': 'Katedra informatiky a kybernetických operací',
            'areal': 'Kasárny Šumavská',
            'building': '3',
            'faculty': [
                { 'id': 23, 'name': 'FVT' }
            ],
            'teachers': [
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
                        fullname
                        areal
                        building
                        faculty: groupsByType(type: 0) {
                            id
                            name
                        }
                        teachers: groupsByType(type: 1) {
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
        <DepartmentLarge {...state} {...props} />
    )
}
*/
function SeznamUcitelu(props) {
    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Vyučující</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul>
                    {props.teachers}
                </ul>
            </Card.Body>
        </div>
    )
}

function ContactInfo(props) {
    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Adresa</Card.Title>
            </Card.Header>
            <Card.Body>
                <b>Areál: </b> {props.areal}<br />
                <b>Budova: </b>{props.building} <br />
            </Card.Body>
        </div>
    )
}