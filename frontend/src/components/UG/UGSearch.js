import Card from "react-bootstrap/Card";

import { useEffect, useState } from "react";


import { UsersByLettersQuery } from "queries/UG/UsersByLettersQuery";
import { GroupsByLettersQuery } from "queries/UG/GroupQuery";


const UserSuggestion = ({user, UserComponent}) => {
    return (
        <li><UserComponent user={user} /></li>
    )
}

const GroupSuggestion = ({group, GroupComponent}) => {
    return (
        <li><GroupComponent group={group} /></li>
    )
}

const Suggestions = ({ userRecords, groupRecords, UserComponent, GroupComponent }) => {

    if ((userRecords.length === 0)&&(groupRecords.length === 0)) {
        return null
    }

    return (
        <div style={{position: "relative"}}>
            <div style={{position: "absolute", top: "0px", zIndex: "10", width: "100%"}}>
                <Card>
                    <Card.Body>
                        <ul>
                            {userRecords.map( 
                                item => <UserSuggestion key={item.id} user={item} UserComponent={UserComponent}/>
                            )}
                            {groupRecords.map( 
                                item => <GroupSuggestion key={item.id} group={item} GroupComponent={GroupComponent}/>
                            )}
                        </ul>
                    </Card.Body>
                </Card>
            </div>
        </div>
    )
}

export const UGSearchSmall = ({users, groups, UserComponent, GroupComponent}) => {
    const [ userRecords, setUserRecords ] =  useState([])
    const [ groupRecords, setGroupRecords ] =  useState([])
    const [ currentLetters, setCurrentLetters ] =  useState('')


    useEffect(() =>{
        if (currentLetters.length > 2) {
            let query = null
            // if (users && groups) {
            //     query = queryAllByLetters
            // } else 
            {
                if (users) {
                    query = UsersByLettersQuery
                } else {
                    query = GroupsByLettersQuery
                }
            }
            query(currentLetters)
            .then(response => response.json())
            // .then(
            //     item => {
            //         console.log(JSON.stringify(item))
            //         return item
            //     }
            // )
            .then(json => {
                const hints = json?.data
                if (hints) {
                    const {users, groups} = hints
                    if (users) {
                        setUserRecords(() => users)
                    }
                    if (groups) {
                        setGroupRecords(() => groups)
                    }
                    
                }
                return json})
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
            <Suggestions userRecords={userRecords} groupRecords={groupRecords} UserComponent={UserComponent} GroupComponent={GroupComponent}/>
        </div>
    )
}

