import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { RolesCard } from 'usersgroups/components/RolesCard';
import { FacultyMedium } from 'usersgroups/components/FacultyMedium';

export const UniversityLarge = (props) => {

    const faculties = props?.subgroups.filter( (item) => item.grouptype.id === "cd49e153-610c-11ed-bf19-001a7dda7110")
    const centers = props?.subgroups.filter( (item) => item.grouptype.id === "cd49e154-610c-11ed-bdbf-001a7dda7110")
    const institutes = props?.subgroups.filter( (item) => item.grouptype.id === "cd49e155-610c-11ed-bdbf-001a7dda7110")

    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    {props.name}
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col md={3}>
                        <RolesCard {...props}/>
                    </Col>
                    <Col md={9}>
                        <Row>
                            {faculties.map(subgroup => <Col md={12}><FacultyMedium {...subgroup}/></Col>)}                    
                        </Row>
                    </Col>
                </Row>
                <Row>
                    <Col md={3}>
                    </Col>
                    <Col md={9}>
                        <Row>
                            {institutes.map(subgroup => <Col md={12}><FacultyMedium {...subgroup}/></Col>)}                    
                        </Row>
                    </Col>
                </Row>
                <Row>
                    <Col md={3}>
                    </Col>
                    <Col md={9}>
                        <Row>
                            {centers.map(subgroup => <Col md={12}><FacultyMedium {...subgroup}/></Col>)}                    
                        </Row>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}