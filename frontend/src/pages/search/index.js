import { Link, useParams } from "react-router-dom";
import Card from "react-bootstrap/Card";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { root } from '../../helpers/index';
import { useQueryGQL, Loading, LoadingError, authorizedFetch } from '../../helpers/index';
import { useEffect, useState } from "react";

export const TeacherSmall = (props) => {
    return (
        <>
        <Link to={root + "/users/teacher/" + (props.id)}>{props.name} {props.surname} </Link>
        <a href={"mailto:" + props.email}><i className="bi bi-envelope"></i></a>
        </>
    )
}

export const GroupSmall = (props) => {
    return (
        <>
        <Link to={root + "/groups/" + (props.id)}>{props.name} {props.surname} </Link>
        </>
    )
}

const Suggestions = (props) => {
    const { userRecords, groupRecords } = props

    if ((userRecords.length == 0)&&(groupRecords.length == 0)) {
        return null
    }

    return (
        <div style={{position: "relative"}}>
        <div style={{position: "absolute", top: "0px", zIndex: "10", width: "100%"}}>
            <Card>
                <Card.Body>
                    <ul>
                        {userRecords.map((item, index) => <li key={item.id}><TeacherSmall  {...item}/></li>)}
                        {groupRecords.map((item, index) => <li key={item.id}><GroupSmall  {...item}/></li>)}
                    </ul>
                </Card.Body>
            </Card>
        </div>
    </div>

    )
}

const queryUsersByLetters = (letters) => 
    authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query($letters: String!) {
                    userByLetters(letters: $letters) {
                    id
                    name
                    surname
                    }
                }`,
            "variables": {"letters": letters}
        }),
    })

const queryGroupsByLetters = (letters) => 
    authorizedFetch('/gql', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        redirect: 'follow', // manual, *follow, error
        body: JSON.stringify({
            "query":
                `query($letters: String!) {
                    groupByLetters(letters: $letters) {
                    id
                    name
                    }
                }`,
            "variables": {"letters": letters}
        }),
    })

export const SearchSmall = (props) => {
    const [ userRecords, setUserRecords ] =  useState([])
    const [ groupRecords, setGroupRecords ] =  useState([])
    const [ currentLetters, setCurrentLetters ] =  useState('')


    useEffect(() =>{
        if (currentLetters.length > 2) {
            queryUsersByLetters(currentLetters).then(
                response => response.json()
            )/*.then(
                item => {
                    console.log(JSON.stringify(item))
                    return item
                }
            )*/.then(
                json => json.data.userByLetters
            ).then(
                dataRecords => setUserRecords(dataRecords)
            )

            queryGroupsByLetters(currentLetters).then(
                response => response.json()
            ).then(
                json => json.data.groupByLetters
            ).then(
                dataRecords => setGroupRecords(dataRecords)
            )
        }
    }, [currentLetters])

    const onChangeInputValue = (p) => {
        console.log(JSON.stringify(p))
        console.log(p.length)
        setCurrentLetters(p)
        if (p.length < 3) {
            setUserRecords([])
        }
    }

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