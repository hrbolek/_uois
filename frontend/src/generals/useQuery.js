import { useEffect, useState } from "react";

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
