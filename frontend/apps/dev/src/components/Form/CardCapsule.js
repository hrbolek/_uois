import Card from "react-bootstrap/Card";

export const CardCapsule = ({title, children}) => 
    <Card>
        <Card.Header>
            <Card.Title>
                {title}
            </Card.Title>
        </Card.Header>
        <Card.Body>
            {children}
        </Card.Body>
    </Card>