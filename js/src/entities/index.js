import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Card from 'react-bootstrap/Card';
import Accordion from "react-bootstrap/Accordion";
import Button from "react-bootstrap/Button";


export const root = '/ui'
export const rootGQL = '/gql'
//export { Students, StudentSmall, StudentLarge, StudentMedium }
//export { TeacherSmall, TeacherMedium, TeacherLarge }


/*
 * @param id holds value for unique entity identification
 * @param queryFunc returns future of response (API) queryFunc = (id) => fetch('api/entity)
 * @param responseToJson is function mapping json retrieved from api to requested data responseToJson = (responseJson) => responseJson.data.data.user
 * @param depends is array of values if a change is detected in array, fetch is rerun
 */
export const useQueryGQL = (id, queryFunc, responseToJson, depends) => {
    const [state, setState] = useState(null);
    const [error, setError] = useState(null);
    useEffect(() =>
        queryFunc(id)
        .then(response => {
            let result = response;
            if (response.status === 200) {
                try {
                    result = response.json()
                } catch (err) {
                    setError('Server response is not json');
                }
            } else {
                result = response.text()
            }
            return result;
        })
        .then(data => {
            let result = data;
            try {
                result = responseToJson(data)
                if (!result) {
                    setError(`Got no data (${result}), check mapping function`)
                }
            } catch (err) {
                setError('Unable to map data, got "' + JSON.stringify(data) + '" from server. Bad query?')
            }
            return result
        })
        .then(data => setState(data))
        .catch(e => setError(e)), depends
    )
    return [state, error];
}

export const LoadingError = (props) =>
    (
        <Card bg='danger' text='white'>
            <Card.Header >{props.error}</Card.Header>
        </Card>
)

export const Loading = (props) => (
    <Card>
        <Card.Header bg='light' text='dark'>Nahrávám</Card.Header>
        <Card.Body>{props.children}</Card.Body>
    </Card>
)

/*
 * @param props.id identification of data entity to be fetched and visualised
 * @param props.query query (async) fetching data from API
 * @param props.responseToJson func for transformation of API response (json) into state data
 * @param props.Visualiser ReactJS component capable to receive selected data and visualise them
 * 
 * if loading is in process, the Loading is displayed
 * if an error occured the LoadingError is displayed
*/
export const Fetching = (props) => {
    const { id, query, Visualiser, responseToJson } = props;
    const [state, error] = useQueryGQL(id, query, responseToJson, [id])
    if (!query || !Visualiser || !responseToJson) {
        <LoadingError error={"Bad use of component Fetching. Missing parameters query and/or Visualiser and/or jsonMapper"} />
    } else {
        if (error != null) {
            return <LoadingError error={error} />
        } else if (state != null) {
            return <Visualiser {...state} />
        } else {
            return <Loading>DataEntity {id}</Loading>
        }
    }
}

export const ExpandableCard = (props) => {
    const { title, children } = props;
    return (
        <Accordion key={0}>
            <Card>
                <Card.Header>
                    <Accordion.Toggle as={Button} variant="link" eventKey={0}>
                        {title}
                    </Accordion.Toggle>
                </Card.Header>
                <Accordion.Collapse eventKey={0}>
                    <Card.Body>
                        {children}
                    </Card.Body>
                </Accordion.Collapse>
            </Card>
        </Accordion>
    )
}

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