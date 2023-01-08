import Card from "react-bootstrap/Card";

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