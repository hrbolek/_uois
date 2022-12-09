import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { DepartmentSmall } from "./department";
//import { PersonSmall } from "../person/person";
import { PersonSmall } from "../person/person";
import { TeacherSmall } from '../person/teacher';
import { root } from '../index';
import { useQueryGQL, Loading, LoadingError } from "../index";
import { ArealSmall } from "../areal/areal";
import { BuildingSmall } from "../areal/building";
import { ProgramSmall } from "../studyprogram/studyprogram";

/** @module Faculty */

export function FacultySmall(props) {
    return (
        <Link to={root + "/groups/faculty/" + props.id}>{props.name}</Link>
    )
}

export function FacultyMedium(props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title>Fakulta <b><FacultySmall {...props} /></b></Card.Title>
            </Card.Header>
            <Card.Body>
                <b>Název:</b> {props.name}<br />
                <b>Děkan:</b> <PersonSmall {...props.dean} /><br />
            </Card.Body>
        </Card>
    )
}

function SeznamProgramu(props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title>Seznam uskutečňovaných programů</Card.Title>
            </Card.Header>
            <Card.Body>
                <ProgramSmall name={'Kybernetická bezpečnost'} id={1} />                
            </Card.Body>
        </Card>
    )
}

/*
                    <Col md={3}>
                        <FacultyMedium {...props} />
                        <ContactInfo {...props} />
                    </Col>
                    <Col md={6}>
                        <SeznamKateder departments={departments} />
                    </Col>
                    <Col md={3}>
                        <SeznamUcitelu teachers={props.members} />
                    </Col>
*/

export function FacultyLarge(props) {
    
    return (
        <Card>
            <Card.Header>
                <h4>Karta fakulty</h4>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={3}>
                        <FacultyMedium {...props} /> <br/>
                        <ContactInfo {...props} />
                    </Col>
                    <Col md={6}>
                        <SeznamKateder {...props} />
                    </Col>
                    <Col md={3}>
                        <SeznamProgramu {...props} />
                    </Col>
                </Row>
            </Card.Body> 
        </Card>
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
        <Card>
            <Card.Header>
                <Card.Title>Adresa</Card.Title>
            </Card.Header>
            <Card.Body>
                <b>Areál: </b> <ArealSmall {...props.areal} /> <br />
                <b>Budova: </b> <BuildingSmall {...props.building} /> <br />
            </Card.Body>
        </Card>
    )
}

function SeznamKateder(props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title>Katedry</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul>
                    {props.departments.map((item) => 
                        (<li key={item.id}><DepartmentSmall key={item.id} {...item} appRoot={props.appRoot} /></li>)
                    )}
                </ul>
            </Card.Body>
        </Card>
    )
}

/**
 * Renders a page with data representing a faculty, contains predefined data which can are overrided by props
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {string} props.name - name
 * @function
 */
export const FacultyLargeStoryBook = (props) => {
    const extendedProps = {
        'id': 1,
        'name': 'FVT',
        'fullname': 'Fakulta vojenských technologií',
        'dean': {'name': 'Vladimír Brzobohatý', 'id': 1 },
        'areal': {'name': 'Kasárna Šumavská', 'id': 1 },
        'building': { 'name': '3', 'id': 1 },
        'departments': [
            { 'id': 4, 'name': 'K-201' },
            { 'id': 5, 'name': 'K-202' },
            { 'id': 6, 'name': 'K-205' },
            { 'id': 7, 'name': 'K-208' },
            { 'id': 8, 'name': 'K-209' },
            { 'id': 9, 'name': 'K-220' }
        ]
    }

    return <FacultyLarge {...extendedProps} {...props} />;
}

/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
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
 * Fetch the data from API endpoint and renders a page representing a faculty
 * @param {*} props - extra props for encapsulated components / visualisers
 * @param {*} [props.as = FacultyLargeStoryBook] - ReactJS component (function) which is responsible for rendering
 * @param {*} [props.with = FacultyLargeQuery] - function fetching the data and returning promise with the data from API endpoint
 * @function
 */
export const FacultyLargeFetching = (props) => {

    const Visualizer = props.as || FacultyLargeStoryBook;
    const queryFunc = props.with || FacultyLargeQuery;

    const [state, error] = useQueryGQL(props.id, queryFunc, (response) => response.data.group, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <Visualizer {...props} {...state} />
    } else {
        return <Loading>Fakulta {props.id}</Loading>
    }

}

export const FacultyPage = (props) => {
    const { id } = useParams();

    return (
        <FacultyLargeFetching {...props} id={id} />
    )       
}