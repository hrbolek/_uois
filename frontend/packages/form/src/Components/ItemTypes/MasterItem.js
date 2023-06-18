import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"

export const MasterItem = ({item}) => {
    return (
        <Row>
            <Col md={2}>
                <b>{item.name} ({item?.type?.name})</b>
            </Col>
            <Col md={10}>
                {item.value}
            </Col>
        
        </Row>
    )
}