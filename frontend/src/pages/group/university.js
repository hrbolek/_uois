import { useEffect, useState, useMemo } from "react";

import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { root } from '../../helpers/index';
import { authorizedFetch } from '../../helpers/index';
import { TeacherSmall } from '../user/teacher';

export const UniversityLargeQuery = (id) =>
    authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!) {
                    groupById(id: $id) {
                        id
                        name
                        roles {
                          roletype {
                            name
                          }
                          user {
                            name
                            surname
                            email
                          }
                        }
                        
                        subgroups {
                          id
                          name
                          grouptype {
                            id
                            name
                          }
                          roles {
                            id
                            roletype {
                            id
                            name
                            }
                            user {
                            id
                            name
                            surname
                            email
                            }
                          }
                        }
                    }
                }`,
            "variables": {"id": id}
        }),
    })

export const RoleRow = (props) => {
    return (
        <Row>
            <Col md={4}><b>{props.roletype.name}</b></Col>
            <Col md={8}>
                <TeacherSmall {...props.user}/>
            </Col>
        </Row>
    )
}

export const FacultyMedium = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    {props.grouptype.name} {props.name}
                </Card.Title>
            </Card.Header>
            <Card.Body>
                {props.roles.map(role => <RoleRow {...role}/>)}
            </Card.Body>
        </Card>
    )
}

export const RolesCard = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Vedoucí pracovníci
                </Card.Title>
            </Card.Header>
            <Card.Body>
                {props.roles.map(role => <RoleRow {...role}/>)}
            </Card.Body>
        </Card>
    )
}

export const UniversityLarge = (props) => {
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Univerzita {props.name}
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={3}>
                        <RolesCard {...props}/>
                    </Col>
                    {props?.subgroups.map(subgroup => <Col md={3}><FacultyMedium {...subgroup}/></Col>)}                    
                </Row>
            </Card.Body>
        </Card>
    )
}