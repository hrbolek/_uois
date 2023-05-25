import Card from 'react-bootstrap/Card';

export const LoadingError = (props) =>
    (
        <Card bg='danger' text='white'>
            <Card.Header >{props.error}</Card.Header>
        </Card>
)
