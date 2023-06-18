import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { BuildingFill, PencilSquare } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"

export const FacilityEditCard = ({facility}) => {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <BuildingFill /> {facility.name}
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={facility.id} tag="facility"><PencilSquare /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>               
                {JSON.stringify(facility)}
            </Card.Body>
        </Card>
    )
}