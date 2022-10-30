import { useCallback, useEffect, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import Card from 'react-bootstrap/Card';
import * as jose from 'jose';

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

/*
 * Login related part
*/
const pseudoStorage = {publicKey: null}

const getPublicKey = () => {
    const publicKey = pseudoStorage?.publicKey
    var promisedPublicKey = null
    if (publicKey === null) {
        promisedPublicKey = fetch('/oauth/publickey', { method: 'GET' })
        .then((response) => {
            let result = null
            if (response.status === 200) {
            try {
                result = response.text()
                pseudoStorage.publicKey = result
            } catch (error) {
            }
            }
            return result
        })
    } else {
        promisedPublicKey = Promise.resolve(publicKey)
    }
    return promisedPublicKey
  } 
  
export const useJWTToken = () => {
    const [token, setToken] = useState(pseudoStorage?.token | localStorage.getItem('token'))

    const wrappedSetToken = useCallback(
        (newToken) => {
            pseudoStorage.token = newToken
            if (newToken === null) {
                localStorage.removeItem('token')
            } else {
                localStorage.setItem('token', newToken)
            }
            setToken(newToken)
        }, 
        [token]
    )

    return [token, wrappedSetToken]

}  

export const authorizedFetch = (path, params={}) => {
    const currentToken = null;
}

export const refreshToken = async () => {
    const refresh_token = localStorage.getItem(refreshToken) | pseudoStorage.refreshToken
    const details = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    };
    const formBody = Object.keys(details).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(details[key])).join('&');

    const response = await fetch('/oauth/token', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body: formBody
    })

    const jwtToken = await response.text()
    const publicKey = await getPublicKey()
    const { payload, protectedHeader } = await jose.jwtVerify(jwtToken, publicKey, {})

    pseudoStorage.accessToken = payload.access_token
    pseudoStorage.refreshToken = payload.refresh_token

    localStorage.setItem('accessToken', payload.access_token)
    localStorage.setItem('refreshToken', payload.refresh_token)

}

export const IncommingLogin = (props) => {
    const [searchParams, setSearchParams] = useSearchParams()
    const code = searchParams.get('code')
    
    useEffect(() => {

        const getTokenFromCode = async () => {
            const details = {
                'code': code,
                'grant_type': 'authorization_code'
            };
            
            const formBody = Object.keys(details).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(details[key])).join('&');

            const response = await fetch('/oauth/token', { 
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
                    },
                    body: formBody
                })

            const jwtToken = await response.text()
                //validate token
            const publicKey = await getPublicKey()
            console.log('got token: ' + jwtToken)
            console.log('got publicKey: ' + publicKey)
            const { payload, protectedHeader } = await jose.jwtVerify(jwtToken, publicKey)

            pseudoStorage.accessToken = payload.access_token
            pseudoStorage.refreshToken = payload.refresh_token

            localStorage.setItem('accessToken', payload.access_token)
            localStorage.setItem('refreshToken', payload.refresh_token)

            console.log('accessToken')
            console.log(JSON.stringify(localStorage.getItem('accessToken')))
        }

        getTokenFromCode();

        return () => {}
    })

    return (<div>we have a code {code}</div>)
}

export const LoginButton = (props) => {
    const navigateToLogin = `${window.location.origin}/ui/login`
    return (
        <>
            <a className="btn btn-primary" href={`/oauth/login?redirect_uri=${navigateToLogin}`}>Login </a>
            {JSON.stringify(localStorage.getItem('accessToken'))}
        </>
        )
}

export const LogoutButton = (props) => {

}