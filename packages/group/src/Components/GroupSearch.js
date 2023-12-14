import Card from "react-bootstrap/Card";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

//import { Loading, LoadingError, authorizedFetch } from 'generals/useQuery';
import { useEffect, useState } from "react";

import { GroupsBy3LettersQuery } from "../Queries/GroupsBy3LettersQuery";
import { Link } from "@uoisfrontend/shared/src/Components/Link";

const GroupSugestion = ({group, onSelect}) => {
    const _onSelect = () => {
        if (onSelect) {
            onSelect(group)
        }
    }
    return (
        <Col>
        <span style={{cursor: "pointer"}} onClick={_onSelect}>{group.name}</span>
        </Col>
    )
}

export const GroupSugestionLink = ({group, onSelect}) => {
    const _onSelect = () => {
        if (onSelect) {
            onSelect(group)
        }
    }
    return (
        <Col>
            <span style={{cursor: "pointer"}} onClick={_onSelect}>
                <Link tag="group" id={group.id}>{group.name}</Link>
            </span>
        </Col>
    )
}

const Suggestions = ({groupRecords, Suggestion, onSelect}) => {
    if ((groupRecords.length === 0)) {
        return null
    }

    return (
        <div style={{position: "relative"}}>
            <div style={{position: "absolute", top: "0px", zIndex: "10", width: "100%"}}>
                <Card>
                    <Card.Body>
                        <Row>
                            {groupRecords.map( 
                                item => <Row><Col key={item.id}>
                                    <Suggestion onSelect={onSelect} group={item}/>
                                </Col></Row>
                            )}
                        </Row>
                    </Card.Body>
                </Card>
            </div>
        </div>
    )
}

export const GroupSearch = ({Suggestion=GroupSugestion, onSelect, label="Vyhledat skupinu", floating=true}) => {
    const [ groupRecords, setGroupRecords ] =  useState([])
    const [ currentLetters, setCurrentLetters ] =  useState('')


    useEffect(() =>{
        if (currentLetters.length > 2) {
            GroupsBy3LettersQuery(currentLetters).then(
                response => response.json()
            )/*.then(
                item => {
                    console.log(JSON.stringify(item))
                    return item
                }
            )*/
            .then(json => json.data)
            .then(hints => {
                if (hints) {
                    setGroupRecords(() => hints.result)
                }
            })
        }
    }, [currentLetters])

    const [inputValue, setInputValue] = useState('')
    const onChange = (e) => {
        const newValue = e.target.value

        setCurrentLetters(newValue)
        if (newValue.length < 3) {
            setGroupRecords([])
        }

        setInputValue(newValue)
    }

    const closeSearch = () => {
        setInputValue('')
        setGroupRecords([])
    }
    
    if (floating) {
        return (
            <div style={{position: "relative"}}>
                <div className="input-group mb-3">
                    <span className="input-group-text" id="basic-addon1"><i className="bi bi-search"></i></span>
                    <div className="form-floating">
                        <input className='form-control' id="groupsearch" placeholder="Vyhledávání skupin" aria-label="Vyhledávání skupin" onChange={onChange} value={inputValue}/>
                        <label htmlFor="groupsearch">{label}</label>    
                    </div>
                    <span className="input-group-text" id="basic-addon2" onClick={closeSearch}><i className="bi bi-x-lg"></i></span>
                </div>
                <Suggestions groupRecords={groupRecords} Suggestion={Suggestion} onSelect={onSelect}/>
    
            </div>
        )
    } else {
        return (
            <div style={{position: "relative"}}>
                <div className="input-group mb-3">
                    <span className="input-group-text" id="basic-addon1"><i className="bi bi-search"></i></span>
                    <input className='form-control' placeholder="Vyhledávání skupin" aria-label="Vyhledávání skupin" onChange={onChange} value={inputValue}/>
                    <span className="input-group-text" id="basic-addon2" onClick={closeSearch}><i className="bi bi-x-lg"></i></span>
                </div>
                <Suggestions groupRecords={groupRecords} Suggestion={Suggestion} onSelect={onSelect}/>
    
            </div>
        )
    }

}