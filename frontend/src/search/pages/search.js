import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { SearchSmall } from "search/components/search"

export const SearchPage = (props) => {
    return (
        <Row>
            <Col></Col>
            <Col>
                <Row>
                    <div style={{'height': '30vh'}}></div>
                </Row>
                <Row>
                    <Col>
                    <Card>
                        <Card.Header>Vyhledávání</Card.Header>
                        <Card.Body>
                            <SearchSmall />
                        </Card.Body>

                    </Card>
                    </Col>
                </Row>
            </Col>
            <Col></Col>
        </Row>
        
    )
}