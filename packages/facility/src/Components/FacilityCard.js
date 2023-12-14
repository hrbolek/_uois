import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { BuildingFill, PencilSquare } from "react-bootstrap-icons"
import { Demo, Link } from "@uoisfrontend/shared"
import { FacilityMap } from "./FacilityMap"
import { FacilitySubfacilitiesTable } from "./FacilitySubfacilitiesTable"

export const FacilityCard = ({facility}) => {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <BuildingFill /> {facility.name} {(facility?.masterFacility) ? <>(<Link tag="facility" id={facility.masterFacility.id}>{facility.masterFacility.name}</Link>)</> : ""}
                    </Col>
                    <Col>
                        {(facility?.group) ? <Link tag="group" id={facility.group.id}>Správci</Link> : ""}
                    </Col>
                    <Col>
                        
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={facility.id} tag="facilityedit"><PencilSquare /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
                <Row>
                    <Col>
                    <Demo />
                {JSON.stringify(facility)}
                        <FacilitySubfacilitiesTable facility={facility} />
                    </Col>
                    <Col>
                        <Card>
                            <Card.Body>
                                <FacilityMap facility={facility} />
                            </Card.Body>
                        </Card>

                        {/* <FacilityMap facility={facility} /> */}
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}