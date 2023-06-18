import { authorizedFetch } from "@uoisfrontend/shared"
import React, { useEffect } from "react"
import Table from "react-bootstrap/Table"
import { useDispatch } from "react-redux"

import All from "@uoisfrontend/shared/src/keyedreducers"
import Button from "react-bootstrap/Button"

export const UserClassificationQueryJSON = (id) => ({
    query: `
    query ($id: ID!) {
        result: userById(id: $id) {
            id
            classifications {
                id
                lastchange
                semester { id}
                level{id name}
                order
                date
            }
        }
      }
    `,
    variables: {id}
})

export const UserClassificationMutationQueryJSON = ({id, lastchange, level_id}) => ({
    query: `
    mutation($id: ID! $lastchange: DateTime! $level_id: ID!) {
        result: classificationUpdate(classification: {
          id: $id,
          lastchange: $lastchange,
          classificationlevelId: $level_id
        }) {
          id
          msg
          classification {
            user {
              id
              name
              surname
              email
              classifications {
                id
                lastchange
                order
                semester { id }
                level { id name }
                date
              }
            }
          }
        }
      }
    `,
    variables: {id, level_id, lastchange}
})

export const UserClassificationQuery = (id) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(UserClassificationQueryJSON(id))
    })

export const UserClassificationMutationQuery = ({id, lastchange, level_id}) => 
    authorizedFetch('/gql', {
        body: JSON.stringify(UserClassificationMutationQueryJSON({id, lastchange, level_id}))
    })

export const UserClassificationFetchAsyncAction = (id) => (dispatch, getState) => {
    UserClassificationQuery(id)
    .then(response => response.json())
    .then(json => {
        const result = json?.data?.result
        if (result) {
            const action = All.ItemSliceActions.item_update(result)
            dispatch(action)
        }
    })

}

export const UserClassificationUpdateAsyncAction = ({id, lastchange, level_id}) => (dispatch, getState) => {
    UserClassificationMutationQuery({id, lastchange, level_id})
    .then(response => response.json())
    .then(json => {
        const result = json?.data?.result
        if (result) {
            const user = result.classification.user
            const action = All.ItemSliceActions.item_update(user)
            dispatch(action)
        }
    })

}

export const UserClassification = ({user}) => {
    const classifications = user?.classifications
    const dispatch = useDispatch()
    useEffect(
        () => {
            if (classifications) {

            } else {
                // console.log("UserClassification.useEffect")
                dispatch(UserClassificationFetchAsyncAction(user.id))
            }
        }, []
    )
    return (
        <UserClassificationsTable user={user} />
    )
}

export const UserClassificationEditable = ({user}) => {
    const classifications = user?.classifications
    const dispatch = useDispatch()
    useEffect(
        () => {
            if (classifications) {

            } else {
                // console.log("UserClassification.useEffect")
                dispatch(UserClassificationFetchAsyncAction(user.id))
            }
        }, []
    )
    return (
        <UserClassificationsTableEditable user={user} />
    )
}

/**
 * 
 * @param {Array} a array which going trought
 * @param {Function} f returns [key, value] for a particular array item
 * @returns dictionary of values
 */
const keyedmap = (a, f) => {
    let result = {}
    a.forEach(
        i => {
            let [key, value] = f(i)
            result[key] = value
        }
    )
    return result
}

/**
 * 
 * @param {Array} a array which going trought 
 * @param {Function} f returns [key, value] for a particular array item
 * @returns dictionary of arrays which represent subarrays of parameter a splitted by keys
 */
const pivotmap = (a, f) => {
    let result = {}
    a.forEach(
        i => {
            let [key, value] = f(i)
            if (key in result) {
                result[key].push(value)
            } else {
                result[key] = [value]
            }            
        }
    )
    return result
}

/**
 * 
 * @param {Object} param0.classification represents a classification (exam result)
 * @returns React.ReactElement - cell (td) of html table
 */
export const UserClassificationCell = ({classification, children}) => {
    return (
        <td>{classification?.level?.name} {children}</td>
)}

/**
 * 
 * @param {Object} param0.classification represents a classification (exam result)
 * @returns React.ReactElement - cell (td) of html table
 */
export const UserSetClassificationButton = ({classification, newlevel}) => {
    const dispatch = useDispatch()
    const onClick =() => {
        dispatch(UserClassificationUpdateAsyncAction({id: classification.id, lastchange: classification.lastchange, level_id: newlevel.id}))
    }
    return (
        // <td>{classification?.level?.name}</td>
        <Button onClick={onClick}>{newlevel.name}</Button>
)}

/**
 * 
 * @param {Object} param0.classifications list of classifications (expected from one semester/subject)
 * @param {Object} param0.cols how many cells must be created
 * @param {React.ReactElement} param0.children cells to be inserted in front of others
 * @returns JSX.Element
 */
export const UserClassificationsRow = ({classifications, children, cols=5}) => {
    const sorted = [...classifications].sort((c1, c2) => c1.order - c2.order)
    const dummy = new Array(cols - 1 - sorted.length).fill('')
    return (
        <tr>
            {children}
            {sorted.map(
                classification => <UserClassificationCell key={classification.id} classification={classification} />
            )}
            {dummy.map(
                (i, index) => (<td key={index}></td>)
            )}
        </tr>
    )}

/**
 * 
 * @param {Object} param0.classifications list of classifications (expected from one semester/subject)
 * @param {Object} param0.cols how many cells must be created
 * @param {React.ReactElement} param0.children cells to be inserted in front of others
 * @returns JSX.Element
 */
export const UserClassificationsRowEditable = ({classifications, children, cols=5}) => {
    const sorted = [...classifications].sort((c1, c2) => c1.order - c2.order)
    const dummy = new Array(cols - 1 - sorted.length).fill('')

    const levelA = {id: '5fae9dd8-b095-11ed-9bd8-0242ac110002', name: 'A'}
    const levelB = {id: '5faea134-b095-11ed-9bd8-0242ac110002', name: 'B'}
    const levelC = {id: '5faea21a-b095-11ed-9bd8-0242ac110002', name: 'C'}
    const levelD = {id: '5faea2d8-b095-11ed-9bd8-0242ac110002', name: 'D'}
    const levelE = {id: '5faea332-b095-11ed-9bd8-0242ac110002', name: 'E'}
    const levelF = {id: '5faea396-b095-11ed-9bd8-0242ac110002', name: 'F'}
    return (
        <tr>
            {children}
            {sorted.map(
                classification => 
                    <UserClassificationCell key={classification.id} classification={classification}>
                        {" "}
                        <UserSetClassificationButton classification={classification} newlevel={levelA}/>{" "}
                        <UserSetClassificationButton classification={classification} newlevel={levelB}/>{" "}
                        <UserSetClassificationButton classification={classification} newlevel={levelC}/>{" "}
                        <UserSetClassificationButton classification={classification} newlevel={levelD}/>{" "}
                        <UserSetClassificationButton classification={classification} newlevel={levelE}/>{" "}
                        <UserSetClassificationButton classification={classification} newlevel={levelF}/>
                    </UserClassificationCell>    
            )}
            {dummy.map(
                (i, index) => (<td key={index}></td>)
            )}
        </tr>
    )}

/**
 * 
 * @param {Object} user datastructure containing a classifications attribute
 * @returns JSX.Element
 */
export const UserClassificationsTable = ({user}) => {
    const classifications = user?.classifications || []
    const classificationsBySemester = pivotmap(
        classifications, classification => [classification.semester.id, classification]
    )   
    const semesterIndex = keyedmap(
        classifications, classification => [classification.semester.id, classification.semester]
    )   
    return (
        <Table>
            <thead>
                <tr>
                    <td>semester</td>
                    <td>1.</td>
                    <td>2.</td>
                    <td>3.</td>
                    <td></td>
                </tr>
            </thead>
            <tbody>
                {Object.entries(classificationsBySemester).map(
                    ([semesterId, clist]) => <UserClassificationsRow key={semesterId} classifications={clist}><td>{semesterIndex[semesterId].order}</td></UserClassificationsRow>
                )}                
            </tbody>
        </Table>
    )
}

/**
 * 
 * @param {Object} user datastructure containing a classifications attribute
 * @returns JSX.Element
 */
export const UserClassificationsTableEditable = ({user}) => {
    const classifications = user?.classifications || []
    const classificationsBySemester = pivotmap(
        classifications, classification => [classification.semester.id, classification]
    )   
    const semesterIndex = keyedmap(
        classifications, classification => [classification.semester.id, classification.semester]
    )   
    return (
        <Table>
            <thead>
                <tr>
                    <td>semester</td>
                    <td>1.</td>
                    <td>2.</td>
                    <td>3.</td>
                    <td></td>
                </tr>
            </thead>
            <tbody>
                {Object.entries(classificationsBySemester).map(
                    ([semesterId, clist]) => <UserClassificationsRowEditable key={semesterId} classifications={clist}><td>{semesterIndex[semesterId].order}</td></UserClassificationsRowEditable>
                )}                
            </tbody>
        </Table>
    )
}
/**
 * 
 * @param {Object} param0.semester datastructure containing a classifications attribute
 * @returns JSX.Element
 */
export const SemesterClassificationsTable = ({semester}) => {
    const classifications = semester?.classifications || []
    const classificationByUser = pivotmap(
        classifications, classification => [classification.user.id, classification])
    const userIndex = keyedmap(
        classifications, classification => [classification.user.id, classification.user]
    )
    return (
        <Table>
            <thead>
                <tr>
                    <td>user</td>
                    <td>1.</td>
                    <td>2.</td>
                    <td>3.</td>
                    <td></td>
                </tr>
            </thead>
            <tbody>
                {Object.entries(classificationByUser).map(
                    ([userId, clist]) => <UserClassificationsRow key={userId} classifications={classifications}><td>{userIndex[userId].email}</td></UserClassificationsRow>
                )}                
            </tbody>
        </Table>
    )
}

// const UserClassificationJSON = [
        
//     {
//       "id": "ce250bd0-b095-11ed-9bd8-0242ac110002",
//       "order": 1,
//       "semester": {
//         "id": "ce250af4-b095-11ed-9bd8-0242ac110002",
//         "order": 1,
//         "subject": {
//           "id": "ce250a68-b095-11ed-9bd8-0242ac110002",
//           "name": "Programování"
//         }
//       },
//       "level": {
//         "name": "F"
//       },
//       "user": {
//         "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
//         "email": "john.newbie@world.com"
//       }
//     },
//     {
//       "id": "ce250bd1-b095-11ed-9bd8-0242ac110002",
//       "order": 2,
//       "semester": {
//         "id": "ce250af4-b095-11ed-9bd8-0242ac110002",
//         "order": 1,
//         "subject": {
//           "id": "ce250a68-b095-11ed-9bd8-0242ac110002",
//           "name": "Programování"
//         }
//       },
//       "level": {
//         "name": "C"
//       },
//       "user": {
//         "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
//         "email": "john.newbie@world.com"
//       }
//     }
// ]

// export const SemesterClassificationsTableConstant = () => {
//     const semester = {classifications: UserClassificationJSON}
//     return (
//         <SemesterClassificationsTable semester={semester} />
//     )
// }

// export const UserClassificationsTableConstant = () => {
//     const user = {classifications: UserClassificationJSON, email: "john@star"}
//     return (
//         <UserClassificationsTable user={user} />
//     )
// }
