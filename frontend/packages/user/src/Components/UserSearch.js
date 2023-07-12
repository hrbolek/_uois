import Card from "react-bootstrap/Card";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

//import { Loading, LoadingError, authorizedFetch } from 'generals/useQuery';
import { useEffect, useState } from "react";

import { UsersBy3LettersQuery } from "../Queries/UsersBy3LettersQuery";
import { Search, XLg } from "react-bootstrap-icons";

const UserSugestion = ({user, onSelect}) => {
    const _onSelect = () => {
        if (onSelect) {
            onSelect(user)
        }
    }
    return (
        <Col>
        <span style={{cursor: "pointer"}} onClick={_onSelect}>{user.name} {user.surname}</span>
        </Col>
    )
}

const Suggestions = ({userRecords, Suggestion, onSelect}) => {
    if ((userRecords.length === 0)) {
        return null
    }

    return (
        <div style={{position: "relative"}}>
            <div style={{position: "absolute", top: "0px", zIndex: "10", width: "100%"}}>
                <Card>
                    <Card.Body>
                        <Row>
                            {userRecords.map( 
                                item => <Row key={item.id}><Col>
                                    <Suggestion onSelect={onSelect} user={item}/>
                                </Col></Row>
                            )}
                        </Row>
                    </Card.Body>
                </Card>
            </div>
        </div>
    )
}

/**
 * 
 * @param {string} props.label 
 * Label to be shown
 * 
 * @returns JSX.Element
 */
export const UserSearch = ({label="Vyhledat uživatele", onSelect, user, clearOnClose=true, floating=true}) => {
    const [ userRecords, setUserRecords ] =  useState([])
    const [ currentLetters, setCurrentLetters ] =  useState(user?(user.name + " " + user.surname):"")


    useEffect(() =>{
        if (currentLetters.length > 2) {
            UsersBy3LettersQuery(currentLetters).then(
                response => response.json()
            )
            .then(json => json.data)
            .then(hints => {
                if (hints) {
                    setUserRecords(() => hints.result)
                }
            })
        }
    }, [currentLetters])

    const [inputValue, setInputValue] = useState(user?(user.name + " " + user.surname):"")
    const onChange = (e) => {
        const newValue = e.target.value
        setCurrentLetters(newValue)
        if (newValue.length < 3) {
            setUserRecords([])
        }
        setInputValue(newValue)
    }

    const closeSearch = () => {
        if (clearOnClose) {
            setInputValue('')           
        }
        setUserRecords([])
    }
    
    if (floating) {
        return (
            <div style={{position: "relative"}}>
                <div className="input-group input-group-sm mb-3">
                    <span className="input-group-text" id="basic-addon1"><Search /></span>
    
                    <div className="form-floating">
                        <input className="form-control form-control-sm" id="usersearch" placeholder="Vyhledávání uživatelů" aria-label="Vyhledávání uživatelů" onChange={onChange} value={inputValue}/>
                        <label htmlFor="usersearch">{label}</label>    
                    </div>
    
                    <span className="input-group-text" id="basic-addon2" onClick={closeSearch}><XLg /></span>
                    
                </div>
                <Suggestions userRecords={userRecords} Suggestion={UserSugestion} onSelect={onSelect}/>
    
            </div>
        )
    } else {
        return (
            <div style={{position: "relative"}}>
                <div className="input-group mb-3">
                    <span className="input-group-text" id="basic-addon1"><Search /></span>   
                    <input className="form-control" id="usersearch" placeholder="Vyhledávání uživatelů" aria-label="Vyhledávání uživatelů" onChange={onChange} value={inputValue}/>
                    <span className="input-group-text" id="basic-addon2" onClick={closeSearch}><XLg /></span>
                </div>
                <Suggestions userRecords={userRecords} Suggestion={UserSugestion} onSelect={onSelect}/>
    
            </div>
        )
    }
    
}