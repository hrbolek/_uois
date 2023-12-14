import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { GearFill, HouseGearFill } from "react-bootstrap-icons"
import { Demo, Link } from "@uoisfrontend/shared"
import { Button } from "react-bootstrap"

export const AdminCard = () => {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <HouseGearFill /> 
                    </Col>
                    <Col>
                        <Link tag="user" id="2d9dc5ca-a4a2-11ed-b9df-0242ac120003">Já</Link>
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        
                    </Col>
                </Row>
                <Card.Title>
                    Administrace
                </Card.Title>

            </Card.Header>
            <Card.Body>
                <Button variant="outline-success"><GearFill /> Role</Button><Button>!</Button>
            </Card.Body>
        </Card>
    )
}