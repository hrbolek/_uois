import { authorizedFetch } from 'generals/authorizedfetch'

export const StudentGroupEvents = (id, startdate, enddate) =>
    authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query ($id: UUID!, $startdate: DateTime!, $enddate: DateTime!) {
                    events: eventByGroup(id: $id, startdate: $startdate, enddate: $enddate) {
                        id, startdate, enddate
                        groups { id, name }
                        organizers { id, name, surname, email }
                }
                }`,
            "variables": {"id": id, "startdate": startdate.toISOString().replace('Z', ''), "enddate": enddate.toISOString().replace('Z', '')}
        }),
    })