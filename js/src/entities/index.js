import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Card from 'react-bootstrap/Card';


export const root = '/ui'
export const rootGQL = '/gql'
//export { Students, StudentSmall, StudentLarge, StudentMedium }
//export { TeacherSmall, TeacherMedium, TeacherLarge }


/*
 * @param id holds value for unique entity identification
 * @param queryFunc returns future of response (API) queryFunc = (id) => fetch('api/entity')
 * @param responseToJson is function mapping json retrieved from api to requested data responseToJson = (responseJson) => responseJson.data.data.user
 * @param depends is array of values if a change is detected in array, fetch is rerun
 */
export const useQueryGQL = (id, queryFunc, responseToJson, depends) => {
    const [state, setState] = useState(null);
    const [error, setError] = useState(null);
    useEffect(() =>
        queryFunc(id)
        .then(response => response.json())
        .then(data => responseToJson(data))
        .then(data => setState(data))
        .catch(e => setError(e)), depends
    )
    return [state, error];
}

export const LoadingError = (props) => (
        <Card>
            <Card.Header bg='danger' text='white'>{props.error}</Card.Header>
        </Card>
)

export const Loading = (props) => (
    <Card>
        <Card.Header bg='light' text='dark'>Nahrávám</Card.Header>
        <Card.Body>{props.children}</Card.Body>
    </Card>
)
/*
export const UpgradeComponentToFetching = (QueryByIdFunc, entityName, Component) =>
    (props) => {
        const [state, setState] = useState(null);
        useEffect(() => QueryByIdFunc(props.id)
            .then(response => response.json())
            .then(data => {
                console.log(JSON.stringify(data))
                return data
            })
            .then(data => setState(data.data['entityName']))
            //.then(data => setState(data.data['entityName']))
            .catch(() => console.log('Error')), [props.id]
            );

        if (state == null) {
            return (<Card>
                <Card.Header>Nahrávám {entityName}</Card.Header>
                <Card.Body>{props.children}</Card.Body>
            </Card>)
        } else {
            return (
                <Component {...state}>{props.children}</Component>
            )
        }
    }

export const UpgradeFetchingToPageWithId = (Component) =>
    (props) => {
        const { id } = useParams();
        return <Component id={id} />
    }
*/