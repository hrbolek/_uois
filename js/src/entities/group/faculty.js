import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import { Card } from "react-bootstrap";
import { DepartmentSmall } from "./department";
import { PersonSmall } from "../persons/person";

import { root } from '../index';
import { useQueryGQL, Loading, LoadingError } from "../index";

export function FacultySmall(props) {
    return (
        <Link to={root + "/groups/faculty/" + props.id}>{props.name}</Link>
    )
}

export function FacultyMedium(props) {
    return (
        <Card className='mb-3'>
            <Card.Header>
                <Card.Title>Fakulta <b><FacultySmall {...props} /></b></Card.Title>
            </Card.Header>
            <Card.Body>
                <b>Název:</b> {props.fullname}<br />
                <b>Děkan:</b> <PersonSmall {...props} name={props.dean} /><br />
            </Card.Body>
        </Card>
    )
}

export function FacultyLarge(props) {
    let departments = props.departments.map((item) => (<li key={item.id}><DepartmentSmall key={item.id} {...item} appRoot={props.appRoot} /></li>))

    return (
        <div className="card w-50">
            <div className="card-header mb-3">
                <h4>Karta fakulty</h4>
            </div>
            <div className='col'>
                <div className='row'>
                    <div className='col'>
                        <FacultyMedium {...props} />
                        <ContactInfo {...props} />
                    </div>
                    <div className='col'>
                        <SeznamKateder departments={departments} />
                    </div>
                </div>
            </div>
        </div>
    )
}

export const FacultyLargeStoryBook = (props) => {
    const extendedProps = {
        'id': props.id,
        'name': props.name,
        'fullname': 'Fakulta vojenských technologií',
        'dean': 'Vladimír Brzobohatý',
        'areal': 'Kasárny Šumavská',
        'building': '3',
        'departments': [
            { 'id': 1, 'name': 'K-201' },
            { 'id': 2, 'name': 'K-202' },
            { 'id': 3, 'name': 'K-205' },
            { 'id': 4, 'name': 'K-208' },
            { 'id': 5, 'name': 'K-209' },
            { 'id': 6, 'name': 'K-220' },
            { 'id': 7, 'name': 'K-221' },
        ]
    }

    return <FacultyLarge {...extendedProps} {...props} />;
}

export const FacultyLargeQuery = (id) => 
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
                group(id: ${id}){
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
                    users {
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

export const FacultyLargeFetching = (props) => {
    const [state, error] = useQueryGQL(props.id, FacultyLargeQuery, (response) => response.data.group, [props.id])
    
    if (state != null) {
        return <FacultyLargeStoryBook {...state} />
    } else if (error != null) {
        return <LoadingError error={error} />
    } else {
        return <Loading>Uživatel {props.id}</Loading>
    }
}

export const FacultyPage = (props) => {
    const { id } = useParams();

    return (
        <FacultyLargeFetching {...props} id={id} />
    )       
}

/*
export function FacultyPage(props) {
    const [state, setState] = useState(
        {
            'id': props.id,
            'name': props.name,
            'fullname': 'Fakulta vojenských technologií',
            'dean': 'Vladimír Brzobohatý',
            'areal': 'Kasárny Šumavská',
            'building': '3',
            'departments': [
                { 'id': 1, 'name': 'K-201' },
                { 'id': 2, 'name': 'K-202' },
                { 'id': 3, 'name': 'K-205' },
                { 'id': 4, 'name': 'K-208' },
                { 'id': 5, 'name': 'K-209' },
                { 'id': 6, 'name': 'K-220' },
                { 'id': 7, 'name': 'K-221' },
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
                        departments: groupsByType(type: 1) {
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
        <FacultyLarge {...state} {...props} />
    )
}
*/

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

function SeznamKateder(props) {
    return (
        <div className="card mb-3">
            <Card.Header>
                <Card.Title>Katedry</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul>
                    {props.departments}
                </ul>
            </Card.Body>
        </div>
    )
}