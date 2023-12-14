import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { SearchSmall } from "./Search"

export const SearchCard = () => {
    // return (
    //     <Card style={{height: "90vh"}}>
    //         <Card.Header>
    //             Vyhledávání
    //         </Card.Header>
    //         <Card.Body>
    //             <Row style={{height: "30vh"}}></Row>
    //             <Row>
    //                 <Col>
    //                 </Col>
    //                 <Col>
    //                     <SearchSmall />
    //                 </Col>
    //                 <Col>
    //                 </Col>
    //             </Row>
    //         </Card.Body>
    //     </Card>
    // )
    return (
        <>
                <Row style={{height: "30vh"}}></Row>
                <Row>
                    <Col>
                    </Col>
                    <Col>
                        <SearchSmall users={true} groups={true}/>
                    </Col>
                    <Col>
                    </Col>
                </Row>
        </>        
    )

}