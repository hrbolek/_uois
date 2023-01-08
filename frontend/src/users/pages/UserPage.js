import { useParams } from 'react-router-dom';
import { useEffect, useMemo } from 'react'
import { configureStore } from '@reduxjs/toolkit'
import { Provider, useDispatch, useSelector } from 'react-redux'

import { UserReducer, updateUserAsync, loadUserAsync } from 'users/reducers/main'

//import { TeacherLarge, TeacherPersonals, TeacherPersonalsEditable } from 'usersgroups/components/TeacherLarge'
import { UserDebug } from 'users/components/UserDebug';
import { TeacherTopMenu } from 'users/components/TeacherTopMenu'
import { AlertsBox } from 'generals/components/AlertsBox';
import { AlertActions, AlertsReducer } from 'generals/reducers/alerts';

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
    }, [dispatch, id])

    //console.log(JSON.stringify(user))
    //console.log(Object.keys(user).length === 0)
    if (!user) {
        return (<>Loading
            <div style={{'position': 'fixed', 'top': '0', 'right': '0', 'width': '100%', 'zIndex': '2180'}}>
                <AlertsBox alerts={alerts} onClose={actions.dismissAlert} />
            </div>        
        </>)
    }

    if (Object.keys(user).length === 0) {
        return (<>Loading
            <div style={{'position': 'fixed', 'top': '0', 'right': '0', 'width': '100%', 'zIndex': '2180'}}>
                <AlertsBox alerts={alerts} onClose={actions.dismissAlert} />
            </div>
        </>)
    }

    //
    return (
        <div>
            <div style={{'position': 'fixed', 'top': '0', 'right': '0', 'width': '100%', 'zIndex': '2180'}}>
                <AlertsBox alerts={alerts} onClose={actions.dismissAlert} />
            </div>
            <UserDebug user={user} actions={actions}/>
        </div>
    )
}

const store = configureStore({ reducer: {user: UserReducer, alerts: AlertsReducer}, preloadedState: {user: {}, alerts: []}})
export const UserPage = (props) => {
    const { id, pageType } = useParams();
    /*const store = useMemo(
        () => configureStore({ reducer: {user: UserReducer, alerts: AlertsReducer}, preloadedState: {user: {}, alerts: []}}),
        [id]
    )
    //*/
    console.log('UserPage', id)
    return (
        <Provider store={store}>
            <TeacherTopMenu />      
            <UserPageDispatcher id={id} pageType={pageType}/>
        </Provider>
    )
}
