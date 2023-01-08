import { useEffect, useState, useMemo } from "react";

import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { root } from '../../helpers/index';
import { authorizedFetch } from '../../helpers/index';
//import { TeacherSmall } from '../user/teacher';

import { TeacherSmall } from 'components/links';
import { FacultyMedium } from 'components/groupcard';


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
                            id
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
    //console.log(JSON.stringify(props))
    return (
        <Row>
            <Col md={4}><b>{props.roletype.name}</b></Col>
            <Col md={8}>
                <TeacherSmall {...props.user}/>
            </Col>
        </Row>
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
                    Univerzit {props.name}
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={3}>
                        <RolesCard {...props}/>
                    </Col>
                    <Col md={9}>
                        <Row>
                            {props?.subgroups.map(subgroup => <Col md={4}><FacultyMedium {...subgroup}/></Col>)}                    
                        </Row>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}