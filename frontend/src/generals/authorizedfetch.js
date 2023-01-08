
const globalFetchParams = {}
export const authorizedFetch = (path, params) => {
    const newParams = {...globalFetchParams, ...params} // allow owerwrite default parameters (globalFetchParams)
    const overridenPath = '/api/gql'
    return (
        fetch(overridenPath, newParams) //params.header should be extended with Authorization TOKEN
    )
}