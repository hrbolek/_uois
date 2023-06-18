import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { HouseFill } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"

export const HomeCard = () => {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <HouseFill />
                    </Col>
                    <Col>
                        <Link tag="user" id="89d1e724-ae0f-11ed-9bd8-0242ac110002">Já</Link>
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>               
                
            </Card.Body>
        </Card>
    )
}