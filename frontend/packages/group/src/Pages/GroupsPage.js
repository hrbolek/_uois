import { Link, authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"
import { useEffect } from "react"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"
import Card from "react-bootstrap/Card"
import { useDispatch, useSelector } from "react-redux"

export const GroupPageQuery = (skip, limit) => ({

})

export const GroupsTypeQueryJSON = (id) => ({
    query: `query($id: ID!) {
        result: groupTypeById(id: $id) {
          __typename
          id
          name
          groups {
            __typename
            id
            name
          }
        }
      }`,
    variables: {id}
})

export const GroupsTypeQuery = (id) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(GroupsTypeQueryJSON(id)),
    })

export const GroupsTypeFetchAsyncAction = (id) => (dispatch, getState) => {
    return (
        GroupsTypeQuery(id)
        .then(response => response.json())
        .then(json => {
            const result = json?.data?.result
            if (result) {
                const action = All.ItemSliceActions.item_update(result)
                dispatch(action)
                for(let group of result.groups) {
                    const action = All.ItemSliceActions.item_update(group)
                    dispatch(action)
                }
            }
            return json
        })
    )
}

export const GroupTypeItems = ({label, groups}) => {
    return (
        <Card>
            <Card.Header>{label}</Card.Header>
            <Card.Body>

            {groups.map(g => <>
                    <span className="btn btn-sm btn-outline-success"><Link tag="group" id={g.id} >{g.name}</Link></span> <br/>
                </>
            )}
            </Card.Body>
        </Card>
    )
}

const unitypeid = "cd49e152-610c-11ed-9f29-001a7dda7110"
const facultytypeid = "cd49e153-610c-11ed-bf19-001a7dda7110"
const insitutetypeid = "cd49e154-610c-11ed-bdbf-001a7dda7110"
const centretypeid = "cd49e155-610c-11ed-bdbf-001a7dda7110"

export const GroupsPage = () => {
    const dispatch = useDispatch()
    const items = useSelector(state => state.items)
    const universities = items[unitypeid] || {name: "", groups: []}
    const faculties = items[facultytypeid] || {name: "", groups: []}
    const institutes = items[insitutetypeid] || {name: "", groups: []}
    const centres = items[centretypeid] || {name: "", groups: []}

    useEffect(
        () => {
            dispatch(GroupsTypeFetchAsyncAction(unitypeid))
            dispatch(GroupsTypeFetchAsyncAction(facultytypeid))
            dispatch(GroupsTypeFetchAsyncAction(insitutetypeid))
            dispatch(GroupsTypeFetchAsyncAction(centretypeid))
        }, []
    )

    return (
        <Row>
            <Col>
            <Card>
                <Card.Body>
                    <GroupTypeItems label={universities.name} groups={universities.groups} />
                    <GroupTypeItems label={faculties.name} groups={faculties.groups} />
                    <GroupTypeItems label={institutes.name} groups={institutes.groups} />
                    <GroupTypeItems label={centres.name} groups={centres.groups} />

                </Card.Body>
            </Card>
            </Col>
        </Row>
    )
}