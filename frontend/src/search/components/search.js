import Card from "react-bootstrap/Card";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

//import { Loading, LoadingError, authorizedFetch } from 'generals/useQuery';
import { useEffect, useState } from "react";

import { queryAllByLetters } from 'search/queries/by3Letters';

//import { GroupSmall, TeacherSmall, UniversitySmall, FacultySmall, DepartmentSmall } from 'usersgroups/components/links'

import { GroupSmall } from "groups/components/links";
import { UserSmall } from "users/components/links";

/*
const groupsVisualizers = [
    { 'id': 'cd49e152-610c-11ed-9f29-001a7dda7110', 'Visualiser': GroupSmall },
    { 'id': 'cd49e153-610c-11ed-bf19-001a7dda7110', 'Visualiser': GroupSmall },
    { 'id': 'cd49e155-610c-11ed-844e-001a7dda7110', 'Visualiser': GroupSmall }
]

const GroupLink = (props) => {
    console.log(JSON.stringify(groupsVisualizers))
    const VisualiserRow = groupsVisualizers.find((visItem) => visItem.id === props.grouptype.id)
    const { Visualiser } = VisualiserRow?VisualiserRow:{ 'id': 'cd49e152-610c-11ed-9f29-001a7dda7110', 'Visualiser': GroupSmall }
    return (
        <li key={props.id}><Visualiser group={props.group}/></li>
    )
}
*/

const Suggestions = (props) => {
    const { userRecords, groupRecords } = props

    if ((userRecords.length === 0)&&(groupRecords.length === 0)) {
        return null
    }

    return (
        <div style={{position: "relative"}}>
            <div style={{position: "absolute", top: "0px", zIndex: "10", width: "100%"}}>
                <Card>
                    <Card.Body>
                        <ul>
                            {userRecords.map( item => <li key={item.id}><UserSmall  user={item}/></li>)}
                            {groupRecords.map( item => <li key={item.id}><GroupSmall group={item} /></li>)}
                        </ul>
                    </Card.Body>
                </Card>
            </div>
        </div>
    )
}

export const SearchSmall = (props) => {
    const [ userRecords, setUserRecords ] =  useState([])
    const [ groupRecords, setGroupRecords ] =  useState([])
    const [ currentLetters, setCurrentLetters ] =  useState('')


    useEffect(() =>{
        if (currentLetters.length > 2) {
            queryAllByLetters(currentLetters).then(
                response => response.json()
            )/*.then(
                item => {
                    console.log(JSON.stringify(item))
                    return item
                }
            )*/.then(
                json => json.data)
            .then(hints => {
                if (hints) {
                    const {userByLetters, groupByLetters} = hints
                    setUserRecords(() => userByLetters)
                    setGroupRecords(() => groupByLetters)    
                }
            })
        }
    }, [currentLetters])

    const [inputValue, setInputValue] = useState('')
    const onChange = (e) => {
        const newValue = e.target.value

        setCurrentLetters(newValue)
        if (newValue.length < 3) {
            setUserRecords([])
        }

        setInputValue(newValue)
    }

    const closeSearch = () => {
        setInputValue('')
        setUserRecords([])
        setGroupRecords([])
    }
    return (
        <div style={{position: "relative"}}>
            <div className="input-group mb-3">
                <span className="input-group-text" id="basic-addon1"><i className="bi bi-search"></i></span>
                <input className='form-control' placeholder="Vyhledávání" aria-label="Vyhledávání" onChange={onChange} value={inputValue}/>
                <span className="input-group-text" id="basic-addon2" onClick={closeSearch}><i className="bi bi-x-lg"></i></span>                
            </div>
            <Suggestions userRecords={userRecords} groupRecords={groupRecords}/>
            
        </div>
    )
}

export const SearchPage = (props) => {
    return (
        <Row>
            <Col>
            </Col>
            <Col>
                <div style={{"height": "40vh"}}></div> <br />
                <SearchSmall {...props} />
            </Col>
            <Col>
            </Col>
        </Row>
    )
}
