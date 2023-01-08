import { useParams } from 'react-router-dom';
import { useState, useEffect, useMemo, useReducer } from 'react'
import { configureStore } from '@reduxjs/toolkit'
import { Provider, useDispatch, useSelector } from 'react-redux'

import { Fetching } from 'generals/components/Fetching'
import { UserSlice, UserReducer, UserActions, updateUserAsync, loadUserAsync } from 'usersgroups/reducers/usermain'

import { TeacherLarge, TeacherPersonals, TeacherPersonalsEditable } from 'usersgroups/components/TeacherLarge'
import { TeacherLargeQuery } from 'usersgroups/queries/teacher'
import { Card } from 'react-bootstrap';
import { useQueryGQL } from 'generals/useQuery';

import { AlertsBox } from 'generals/components/AlertsBox';
import { AlertActions, AlertsReducer } from 'generals/reducers/alerts';

export const UserPage_ = (props) => {
    const { id, pageType } = useParams();
/*
        Visualiser: UniversityLarge,
        query: UniversityLargeQuery,
        selector: json => json.data.groupById

*/
    return (
        
        <Fetching id={id} Visualiser={TeacherLarge} selector={json => json.data.userById} query={TeacherLargeQuery}/>
        
    )
}

const UserPageDispatcher = (props) => {
    const dispatch = useDispatch()
    const user = useSelector(state => state.user)
    const alerts = useSelector(state => state.alerts)
    const id = props.id
    const actions = useMemo(
        () => ({
            'updateUser': (newUser) => {
                //console.log('updateUser')
                dispatch(updateUserAsync(newUser))
            },
            'dismissAlert': (id) => {
                dispatch(AlertActions.RemoveAlert({id}))
            }
        }), [dispatch]
    )

    useEffect( () => {
        dispatch(loadUserAsync({id: id}))
    }, [id])

    //console.log(JSON.stringify(user))
    //console.log(Object.keys(user).length === 0)
    if (Object.keys(user).length === 0) {
        return (<>Loading</>)
    }
    return (
        <div>
            <TeacherPersonalsEditable user={user} actions={actions}/>
            <AlertsBox alerts={alerts} onClose={actions.dismissAlert} />
        </div>
    )
}

const userStore = configureStore({ reducer: {user: UserReducer, alerts: AlertsReducer}, preloadedState: {user: {}, alerts: []}})
export const UserPage = (props) => {
    const { id, pageType } = useParams();
    return (
        <Provider store={userStore}>
            <UserPageDispatcher id={id} pageType={pageType}/>
        </Provider>
    )
}
