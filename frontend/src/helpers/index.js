import { useCallback, useEffect, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";
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

const getPublicKey = async () => {
    let publicKey = pseudoStorage?.publicKey
    var promisedPublicKey = null
    if (publicKey === null) {
        const response = await fetch('/oauth/publickey', { method: 'GET' })
        const text = await response.text()
        publicKey = text.replaceAll('\\n', '\n').replaceAll('"', '')
        pseudoStorage.publicKey = publicKey
    } 
    return publicKey
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
    const navigate = useNavigate();
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

            let jwtToken = (await response.text()).replaceAll('"', '')
                //validate token
            let publicKey = await getPublicKey()
            //console.log('got token: ' + jwtToken)
            //console.log('got publicKey: ' + publicKey)
            //console.log('got token: ' + (typeof jwtToken))
            //console.log('got publicKey: ' + (typeof publicKey))

            //*
            //const jwtTokenF = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiQmVhcmVyIiwiYWNjZXNzX3Rva2VuIjoiQUNDVC1XTk1wM1U5NTZtMjRiSEEwaHFHdm81aGc5QW9FOHA2dSIsImV4cGlyZXNfaW4iOjM2MDAsInJlZnJlc2hfdG9rZW4iOiJSRUZULWJPY2xkS1lic0FxUW5UQUs5YWxOR0pUWkN0YzBWVXNPIn0.LN7gZP0z2f975UzrE4Hx5mocA7LGMMMhcbfVvO_GJdEiOZqBgcXqbFDELdUvkWaYTv2vRaBHScJottIXkU_WMbPR0l5NiPrvkkXfOxz_rPzE2UvLtdanFL0CmHXFGhBsNZCuVgwe3LUTEbS7ut65jlzqZDR7BsJZewg_l3ziU6Qbhmtw97RKh9kOm6rQ-zlT0DNRjdLqcujjSCOPXG84V7HVHY3A-q490S1JHfFn_iYvTtw92_xpGu8JlVA0PpzeN-ACwYYND_oc2iinlEwYvcRm9i7n5keppt0h4J4zA8RAmk2D_ygfyk_hxoUZGV4yfdn_SzOFaZ9n4DiadhIzGA"
            //const publicKeyF = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAowso+zTvN9zUbSefa+dU\nIu1gumwOvutgq1t44ewkHAPgLmHvUUyUMVQ2O/qVjj1javSdbSC5+v2k8lZYrxvt\nAetznGGmc4iGBF4AUv3xbga4yCethbWZN5wzAyj+ABIluY9iWh5HglcGNymohvOB\nhCci/MMNP5cSRH0JpgW8q/LyVuaH8gQ9ZWQNTIInCstMA1ZVf7ftNc7OHI4qU8gV\nLaoGTqhk7XawnDeinXTUznH8OhXucOvbzW8Uhf3vuoNpaVTygm5GIbMn84D0gU2r\nnZYOWaqQXMgSOe4zF+nzxD+g9lsfqWd7LoATsc+EZ7BLKjULgmXH5EyrgXv6kAd1\n6QIDAQAB\n-----END PUBLIC KEY-----\n" 
            //*/

            //console.log('got token: ' + (jwtToken === jwtTokenF))
            //console.log('got publicKey: ' + (publicKey === publicKeyF))

            //jwtToken = `${jwtToken}`
            //publicKey = `${publicKey}`

            //console.log('got token: ' + (jwtTokenF))
            //console.log('got publicKey: ' + (publicKeyF))
            //const claims = jose.decodeJwt(token)
            //console.log(claims)
            
            const publicKeyObject = await jose.importSPKI(publicKey, "RS256")
            //const verifyResult = jose.verify(jose.deserialize_compact(jwt), jwk, 'HS256')
            //const verifyResult = await jose.compactVerify(jwtToken, publicKey, {algorithm:  ["RS256"]})
            //console.log(JSON.stringify(verifyResult))
            
            const { payload, protectedHeader } = await jose.jwtVerify(jwtToken, publicKeyObject, {algorithm:  ["RS256"]})

            pseudoStorage.accessToken = payload.access_token
            pseudoStorage.refreshToken = payload.refresh_token

            localStorage.setItem('accessToken', payload.access_token)
            localStorage.setItem('refreshToken', payload.refresh_token)
            
            console.log('accessToken')
            console.log(JSON.stringify(localStorage.getItem('accessToken')))
        }

        getTokenFromCode();


        navigate('/ui/api')
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