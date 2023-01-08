import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { RolesCard } from 'usersgroups/components/RolesCard';
import { FacultyMedium } from 'usersgroups/components/FacultyMedium';

import { UniversitySmall, FacultySmall, DepartmentSmall } from 'usersgroups/components/links'

export const FacultyLarge = (props) => {
    const katedry = props?.subgroups.filter(item => item.grouptype.id == "cd49e155-610c-11ed-844e-001a7dda7110")
    const studG = props?.subgroups.filter(item => item.grouptype.id == "cd49e157-610c-11ed-9312-001a7dda7110")
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <UniversitySmall {...props.mastergroup} /> / {props.name}
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={3}>
                        <RolesCard {...props}/>
                    </Col>
                    <Col md={4}>
                        <Card>
                            <Card.Header>
                                <Card.Title>Katedry</Card.Title>
                            </Card.Header>
                            <Card.Body>
                                {katedry.map(subgroup => <><DepartmentSmall {...subgroup}/><br /></>)}
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col md={4}>
                        <Card>
                            <Card.Header>
                                <Card.Title>Studijní skupiny</Card.Title>
                            </Card.Header>
                            <Card.Body>
                                <Row>
                                {studG.map(subgroup => <Col md={4}>{subgroup.name}</Col>)}
                                </Row>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
                <Row>
                    
                </Row>
            </Card.Body>
        </Card>
    )
}