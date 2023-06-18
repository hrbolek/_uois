// import { authorizedFetch } from "@uoisfrontend/shared"
// import React from "react"
// import Table from "react-bootstrap/Table"
// import { useDispatch } from "react-redux"

// /**
//  * 
//  * @param {Array} a array which going trought
//  * @param {Function} f returns [key, value] for a particular array item
//  * @returns dictionary of values
//  */
// const keyedmap = (a, f) => {
//     let result = {}
//     a.forEach(
//         i => {
//             let [key, value] = f(i)
//             result[key] = value
//         }
//     )
//     return result
// }

// /**
//  * 
//  * @param {Array} a array which going trought 
//  * @param {Function} f returns [key, value] for a particular array item
//  * @returns dictionary of arrays which represent subarrays of parameter a splitted by keys
//  */
// const pivotmap = (a, f) => {
//     let result = {}
//     a.forEach(
//         i => {
//             let [key, value] = f(i)
//             if (key in result) {
//                 result[key].push(value)
//             } else {
//                 result[key] = [value]
//             }            
//         }
//     )
//     return result
// }

// /**
//  * 
//  * @param {Object} param0.classification represents a classification (exam result)
//  * @returns React.ReactElement - cell (td) of html table
//  */
// export const UserClassificationCell = ({classification}) => {
//     return (
//         <td>{classification?.level?.name}</td>
// )}


// const SetWserClassificationAsyncAction = ({user, semester, level}) => (dispatch, geState) => {
//     authorizedFetch()
//     .then(response => response.json())
//     .then(json => {
//         const msg = json?.result?.msg 
//         if (msg === "ok") {
//             const user = json.result.classification.user
//             dispatch()
//         }
//     })
// }

// /**
//  * 
//  * @param {Object} param0.classification represents a classification (exam result)
//  * @returns React.ReactElement - cell (td) of html table
//  */
// export const UserClassificationCellEditable = ({classification}) => {
//     const dispatch = useDispatch()
//     const onClick =() => {
//         dispatch(SetWserClassificationAsyncAction({user, semester, level: "F"}))
//     }
//     return (
//         // <td>{classification?.level?.name}</td>
//         <td>{classification?.level?.name}<button>F</button></td>
// )}

// /**
//  * 
//  * @param {Object} param0.classifications list of classifications (expected from one semester/subject)
//  * @param {Object} param0.cols how many cells must be created
//  * @param {React.ReactElement} param0.children cells to be inserted in front of others
//  * @returns 
//  */
// export const UserClassificationsRow = ({classifications, children, cols=5}) => {
//     const sorted = [...classifications].sort((c1, c2) => c1.order - c2.order)
//     const dummy = new Array(cols - 1 - sorted.length).fill('')
//     return (
//         <tr>
//             {children}
//             {sorted.map(
//                 classification => <UserClassificationCell key={classification.id} classification={classification} />
//             )}
//             {dummy.map(
//                 (i, index) => (<td key={index}></td>)
//             )}
//         </tr>
//     )}

// /**
//  * 
//  * @param {Object} user datastructure containing a classifications attribute
//  * @returns 
//  */
// export const UserClassificationsTable = ({user}) => {
//     const classifications = user?.classifications || []
//     const classificationsBySemester = pivotmap(
//         classifications, classification => [classification.semester.id, classification]
//     )   
//     const semesterIndex = keyedmap(
//         classifications, classification => [classification.semester.id, classification.semester]
//     )   
//     return (
//         <Table>
//             <thead>
//                 <tr>
//                     <td>semester</td>
//                     <td>1.</td>
//                     <td>2.</td>
//                     <td>3.</td>
//                     <td></td>
//                 </tr>
//             </thead>
//             <tbody>
//                 {Object.entries(classificationsBySemester).map(
//                     ([semesterId, clist]) => <UserClassificationsRow key={semesterId} classifications={clist}><td>{semesterIndex[semesterId].order}</td></UserClassificationsRow>
//                 )}                
//             </tbody>
//         </Table>
//     )
// }

// /**
//  * 
//  * @param {Object} param0.semester datastructure containing a classifications attribute
//  * @returns 
//  */
// export const SemesterClassificationsTable = ({semester}) => {
//     const classifications = semester?.classifications || []
//     const classificationByUser = pivotmap(
//         classifications, classification => [classification.user.id, classification])
//     const userIndex = keyedmap(
//         classifications, classification => [classification.user.id, classification.user]
//     )
//     return (
//         <Table>
//             <thead>
//                 <tr>
//                     <td>user</td>
//                     <td>1.</td>
//                     <td>2.</td>
//                     <td>3.</td>
//                     <td></td>
//                 </tr>
//             </thead>
//             <tbody>
//                 {Object.entries(classificationByUser).map(
//                     ([userId, clist]) => <UserClassificationsRow key={userId} classifications={classifications}><td>{userIndex[userId].email}</td></UserClassificationsRow>
//                 )}                
//             </tbody>
//         </Table>
//     )
// }

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

