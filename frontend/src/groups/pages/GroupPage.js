import { useParams } from 'react-router-dom';
import { useEffect, useMemo } from 'react'
import { configureStore } from '@reduxjs/toolkit'
import { Provider, useDispatch, useSelector } from 'react-redux'

import { GroupReducer, GroupActions, loadGroupAsync, updateGroupAsync, updateGroupInTreeAsync, extendGroupAsync } from 'groups/reducers/main'
import { GroupLargeQuery, GroupBaseQuery, DepartmentLargeQuery, FacultyLargeQuery } from 'groups/queries/group'
import { GroupDebug } from 'groups/components/GroupDebug'
import { GroupTopMenu } from 'groups/components/GroupTopMenu'

import { AlertsBox } from 'generals/components/AlertsBox';
import { AlertActions, AlertsReducer } from 'generals/reducers/alerts';

const GroupPageDispatcher = (props) => {
    const dispatch = useDispatch()
    const group = useSelector(state => state.group)
    const grouptypeid = group.grouptype?.id
    const alerts = useSelector(state => state.alerts)
    const id = props.id
    const actions = useMemo(
        () => ({
            'updategroup': (newGroup) => {
                //console.log('updateGroup')
                dispatch(updateGroupAsync(newGroup))
            },
            'dismissAlert': (id) => {
                dispatch(AlertActions.RemoveAlert({id}))
            },
            'updateGroupInTreeAsync': (group) => {
                dispatch(updateGroupInTreeAsync(group))
            }
        }), [dispatch]
    )

    useEffect( () => {
        dispatch(GroupActions.setGroup({}));
        dispatch(loadGroupAsync({id: id}, GroupBaseQuery))
    }, [dispatch, id])
//*
    useEffect( () => {
        console.log(grouptypeid)
        if (group?.grouptype) {
            if (group?.grouptype.id === "cd49e155-610c-11ed-844e-001a7dda7110") {//katedra
                dispatch(extendGroupAsync({id: id}, DepartmentLargeQuery))
            } if (group?.grouptype.id === "cd49e153-610c-11ed-bf19-001a7dda7110") {//ustav
                dispatch(extendGroupAsync({id: id}, FacultyLargeQuery))
            } if (group?.grouptype.id === "cd49e153-610c-11ed-bf19-001a7dda7110") {//fakulta
                dispatch(extendGroupAsync({id: id}, FacultyLargeQuery))
            } if (group?.grouptype.id === "cd49e155-610c-11ed-bdbf-001a7dda7110") {//centrum
                dispatch(extendGroupAsync({id: id}, FacultyLargeQuery))
            } if (group?.grouptype.id === "cd49e157-610c-11ed-9312-001a7dda7110") {//studijni skupina
                dispatch(extendGroupAsync({id: id}, DepartmentLargeQuery))
            } else {
                //dispatch(loadGroupAsync({id: id}, DepartmentLargeQuery))
            }
        }
    }, [grouptypeid])
//*/
    //console.log(JSON.stringify(group))
    //console.log(Object.keys(group).length === 0)
    if (Object.keys(group).length === 0) {
        return (
        <>Loading
            <div style={{'position': 'fixed', 'top': '0', 'right': '0', 'width': '100%', 'zIndex': '2180'}}>
                <AlertsBox alerts={alerts} onClose={actions.dismissAlert} />
            </div>

        </>)
    }
    return (
        <div>
            
            <GroupDebug group={group} actions={actions} />
            <div style={{'position': 'fixed', 'top': '0', 'right': '0', 'width': '100%', 'zIndex': '2180'}}>
                <AlertsBox alerts={alerts} onClose={actions.dismissAlert} />
            </div>
        </div>
    )
}

const store = configureStore({ reducer: {group: GroupReducer, alerts: AlertsReducer}, preloadedState: {group: {}, alerts: []}})
export const GroupPage = (props) => {
    const { id, pageType } = useParams();
    /*const store = useMemo(
        () => configureStore({ reducer: {group: GroupReducer, alerts: AlertsReducer}, preloadedState: {group: {}, alerts: []}}),
        [id]
    )
    //*/
    return (
        <Provider store={store}>
            <GroupTopMenu />
            <GroupPageDispatcher id={id} pageType={pageType} />
        </Provider>
    )
}
