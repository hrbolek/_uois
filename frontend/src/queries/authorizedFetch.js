const globalFetchParams = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    redirect: 'follow', // manual, *follow, error
}

/**
 * Zapouzdrujici funkce pro fetch, vytvari mezi vrstvu pro komunikace ze serverem
 * @param {*} path 
 * @param {*} params 
 * @returns 
 */
export const authorizedFetch = (path, params) => {
    const newParams = {...globalFetchParams, ...params} // allow owerwrite default parameters (globalFetchParams)
    const overridenPath = '/api/gql'
    return (
        fetch(overridenPath, newParams) //params.header should be extended with Authorization TOKEN
    )
}
