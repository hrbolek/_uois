import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { TeacherSmall } from "../person/teacher";
import { FacultySmall } from "./faculty";

import { root } from '../index';
import { useQueryGQL, Loading, LoadingError } from "../index";
import { ArealSmall } from "../areal/areal";
import { BuildingSmall } from "../areal/building";

/** @module Department */

export function DepartmentSmall(props) {
    return (
        <Link to={root + "/groups/department/" + props.id}>{props.name}</Link>
    )
}

export function DepartmentMedium(props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title>Katedra <b><DepartmentSmall {...props} /></b></Card.Title>
            </Card.Header>
            <Card.Body>
                <b>Název:</b> {props.fullname}<br />
                <b>Vedoucí katedry:</b> {props.VK}<br />
                <b>Fakulta:</b> <FacultySmall {...props.faculty}/><br />
            </Card.Body>
        </Card>
    )
}


function SeznamUcitelu(props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title>Vyučující</Card.Title>
            </Card.Header>
            <Card.Body>
                <ul>
                    {props.members.map(
                        (item, index) => (<li key={index}><TeacherSmall key={item.id} {...item} /></li>)
                        )
                    }
                </ul>
            </Card.Body>
        </Card>
    )
}

function ContactInfo(props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title>Adresa</Card.Title>
            </Card.Header>
            <Card.Body>
                <b>Areál: </b> <ArealSmall {...props.areal} /><br />
                <b>Budova: </b> <BuildingSmall {...props.building} /> <br />
            </Card.Body>
        </Card>
    )
}
export const DepartmentVaV = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>Vav link</Card.Title>
            </Card.Header>
            <Card.Body>
                <a href={'https://vav.unob.cz/department/index/114'}>VaV</a><br/>
                <a href={'https://vav.unob.cz/results/department/114'}>VaV výsledky</a><br/>
                <a href={'https://vav.unob.cz/department/projects/114'}>VaV projekty</a>
                
            </Card.Body>
        </Card>
    )
}
export function DepartmentLarge(props) {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Karta katedry
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={3}>
                        <DepartmentMedium {...props} /> <br/>
                        <ContactInfo {...props} />
                    </Col>
                    <Col md={6}>
                    </Col>
                    <Col md={3}>
                        <SeznamUcitelu {...props}/> <br/>
                        <DepartmentVaV {...props}/>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
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


/*

    const Visualizer = props.as || TeacherLargeStoryBook;
    const queryFunc = props.with || TeacherLargeQuery;
*/

/**
 * Renders a page with data representing a department, contains predefined data which can are overrided by props
 * @param {*} props 
 * @param {*} props.id - identification
 * @param {string} props.name - name
 * @function
 */
export const DepartmentLargeStoryBook = (props) => {
    const extendedProps = {
        'id': props.id,
        'name': props.name,
        'fullname': 'Katedra informatiky a kybernetických operací',
        'areal': {'name': 'Kasárna Šumavská', 'id': 1 },
        'building': {'name': 'KŠ3', 'id': 1},
        'faculty': { 'id': 23, 'name': 'FVT' },
        'members': [
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

/**
 * Retrieves the data from GraphQL API endpoint
 * @param {*} id - identificator
 * @function
 */
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
 * Fetch the data from API endpoint and renders a page representing a department
 * @param {*} props - extra props for encapsulated components / visualisers
 * @param {*} [props.as = DepartmentLargeStoryBook] - ReactJS component (function) which is responsible for rendering
 * @param {*} [props.with = DepartmentLargeQuery] - function fetching the data and returning promise with the data from API endpoint
 * @function
 */
export const DepartmentLargeFetching = (props) => {

    const Visualizer = props.as || DepartmentLargeStoryBook;
    const queryFunc = props.with || DepartmentLargeQuery;

    const [state, error] = useQueryGQL(props.id, queryFunc, (response) => response.data.group, [props.id])
    
    if (error != null) {
        return <LoadingError error={error} />
    } else if (state != null) {
        return <Visualizer {...props} {...state} />
    } else {
        return <Loading>Katedra {props.id}</Loading>
    }
}

export const DepartmentPage = (props) => {
    const { id } = useParams();

    return (
        <DepartmentLargeFetching {...props} id={id} />
    )       
}