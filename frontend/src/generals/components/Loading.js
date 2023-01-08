import Card from 'react-bootstrap/Card';

export const Loading = (props) => (
    <Card>
        <Card.Header bg='light' text='dark'>Nahrávám</Card.Header>
        <Card.Body>{props.children}</Card.Body>
    </Card>
)
