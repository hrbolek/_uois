import Card from "react-bootstrap/Card";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

//import { Loading, LoadingError, authorizedFetch } from 'generals/useQuery';
import { useEffect, useState } from "react";

import { FacilitysBy3LettersQuery } from "../Queries/FacilityBy3LettersQuery";

const FacilitySugestion = ({facility, onSelect}) => {
    const _onSelect = () => {
        if (onSelect) {
            onSelect(facility)
        }
    }
    return (
        <Col>
            <span onClick={_onSelect}>{facility.name}</span>
        </Col>
    )
}

const Suggestions = ({facilityRecords, Suggestion, onSelect}) => {
    if ((facilityRecords.length === 0)) {
        return null
    }

    return (
        <div style={{position: "relative"}}>
            <div style={{position: "absolute", top: "0px", zIndex: "10", width: "100%"}}>
                <Card>
                    <Card.Body>
                        <Row>
                            {facilityRecords.map( 
                                item => <Row><Col key={item.id}>
                                    <Suggestion onSelect={onSelect} facility={item}/>
                                </Col></Row>
                            )}
                        </Row>
                    </Card.Body>
                </Card>
            </div>
        </div>
    )
}

export const FacilitySearch = ({onSelect, label="Vyhledat místo", floating=true}) => {
    const [ facilityRecords, setFacilityRecords ] =  useState([])
    const [ currentLetters, setCurrentLetters ] =  useState('')


    useEffect(() =>{
        if (currentLetters.length > 2) {
            FacilitysBy3LettersQuery(currentLetters).then(
                response => response.json()
            )
            /*.then(
                item => {
                    console.log(JSON.stringify(item))
                    return item
                }
            )*/
            .then(json => json.data)
            .then(hints => {
                if (hints) {
                    setFacilityRecords(() => hints.result)
                }
            })
        }
    }, [currentLetters])

    const [inputValue, setInputValue] = useState('')
    const onChange = (e) => {
        const newValue = e.target.value

        setCurrentLetters(newValue)
        if (newValue.length < 3) {
            setFacilityRecords([])
        }

        setInputValue(newValue)
    }

    const closeSearch = () => {
        setInputValue('')
        setFacilityRecords([])
    }

    let Encapsulate = ({children}) => <>{children}</>
    if (floating) {
        Encapsulate = ({children}) => <div className="form-floating">
                {children}
                <label htmlFor="facilitysearch">{label}</label>    
            </div>
    }

    return (
        <div style={{position: "relative"}}>
            <div className="input-group mb-3">
                <span className="input-group-text" id="basic-addon1"><i className="bi bi-search"></i></span>

                <Encapsulate>
                    <input className='form-control' id="facilitysearch" placeholder="Vyhledávání prostor" aria-label="Vyhledávání prostor" onChange={onChange} value={inputValue}/>                   
                </Encapsulate>

                <span className="input-group-text" id="basic-addon2" onClick={closeSearch}><i className="bi bi-x-lg"></i></span>
            </div>
            <Suggestions facilityRecords={facilityRecords} Suggestion={FacilitySugestion} onSelect={onSelect}/>
        </div>
    )
   
}