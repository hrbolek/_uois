import { createSlice } from '@reduxjs/toolkit'

import { GroupUpdateQuery, groupLargeQuery, GroupBaseQuery } from 'groups/queries/group'
import { AlertActions } from 'generals/reducers/alerts';
export const CreateDelayer = (delay=300) => {
    //lokalni promenna
    let oldTimer = -1;
    let state = 0;

    //navratovou hodnotou je funkce umoznujici zpozdeni volani
    return (delayedFunc, callback = () => null) => {
        /*
        //https://stackoverflow.com/questions/26150232/resolve-javascript-promise-outside-the-promise-constructor-scope
        implement as function returning a Promise:

        const main = () => {
            let resolver = null
            const result = new Promise((resolve, reject) => {resolver = resolve})
            resolver(25)
            return result
        }

        main().then(data=>{console.log('a', data)})
        */
        //zruseni stareho timeru
        if (state !== 0) {
            clearTimeout(oldTimer)
            oldTimer = -1;
            state = 0;
        }
        
        //zabaleni funkce, pri volani je poznamenano, ze byl volan
        const encapsulatedFunc = () => {
            oldTimer = -1;
            state = 0;
            delayedFunc();
            callback(); // volani "after" funkce, v podstate notifikace, ze "done"
        }

        //ocekavame zpozdene volani funkce
        state = 1;

        //definice noveho timeru
        oldTimer = setTimeout(encapsulatedFunc, delay);
    }
}

const findGroupInState = (state, group) => {
    if (state.id === group.id) {
        return state
    }
    if (state.subgroups) {
        const result = state.subgroups.find(sg => findGroupInState(sg, group))
        //console.log('findGroupInState', result)
        return result
    } 
    return undefined
}

const invalidateGroupDelayer = CreateDelayer()
export const updateGroupInTreeAsync = (group) => (dispatch, getState) => {
    const state = getState()
    const currentGroup = findGroupInState(state.group, group)
    
    if (currentGroup === undefined) {
        dispatch(AlertActions.AddAlert({'main': 'Chyba', 'explain': `${JSON.stringify(group)} nenalezena v ulozisti`, 'type': 'alert-danger'}))
    } else {
        //console.log('updateGroupInTreeAsync', currentGroup)
        dispatch(GroupActions.updateGroupInTree(group))

        //opravit
        const groupWithLastchange = {...currentGroup, ...group}
        const updateGQL = () => GroupUpdateQuery(groupWithLastchange)
        .then(response => response.json())
        .then(json => {
            if (json.errors) {
                dispatch(AlertActions.AddAlert({'main': 'Chyba uložení', 'explain': json.errors[0].message, 'type': 'alert-danger'}))
            } else {
                const updateResult = json.data.groupById.editor.update
                const resultStatus = updateResult.result
                const changedGroup = updateResult.group

                if (resultStatus === "ok") {

                    console.log('resultStatus === "ok"', groupWithLastchange.lastchange, changedGroup.lastchange)

                    // data byla skutecne ulozena
                    dispatch(AlertActions.AddAlert({'main': 'Ok', 'explain': 'Změny uloženy', 'type': 'alert-success'}))
                    // poznamenat si lastchange pro příští uložení
                    dispatch(GroupActions.updateGroupInTree({...group, 'lastchange': changedGroup.lastchange}))

                } else {
                    // data se nepodarilo ulozit, ale odpoved od serveru doputovala

                    console.log('resultStatus !== "ok"', groupWithLastchange.lastchange, changedGroup.lastchange)

                    const overwriteFunc = () => {
                        //musime zmenit lastchange in state
                        dispatch(GroupActions.updateGroupInTree({...group, 'lastchange': changedGroup.lastchange}))
                        //retry save
                        dispatch(updateGroupInTreeAsync({...group}))
                    }
                    const acceptFunc = () => {
                        //accept server state
                        console.log(changedGroup)
                        console.log(getState())
                        dispatch(GroupActions.updateGroupInTree({...changedGroup}))
                        console.log(getState())
                    }
                    dispatch(AlertActions.AddAlert(
                        {
                            'main': 'Ok', 'explain': 'Někdo na serveru provedl změnu, chcete ji přepsat?', 'type': 'alert-danger', 
                            'extraButtons': [
                                {'props': {'className': 'btn btn-warning'}, 'onClick': overwriteFunc, 'label': 'Vynutit přepsání'},
                                {'props': {'className': 'btn btn-warning'}, 'onClick': acceptFunc, 'label': 'Převzít data ze serveru'}
                            ]
                        }
                    ))                    
                }
            }
            return json
        })
        .catch((e) => dispatch(AlertActions.AddAlert({'main': 'Chyba uložení', 'explain': e, 'type': 'alert-danger'})))

        invalidateGroupDelayer(updateGQL)
    }
}

const updateGroupDelayer = CreateDelayer()
export const updateGroupAsync = (group) => (dispatch, getState) => {
    const state = getState()
    //console.log(JSON.stringify(state))
    const currentGroup = state.group
    //const limitedGroup = { name: currentGroup.name, valid: currentGroup.valid }
    const newAction = { lastchange: currentGroup.lastchange, ...group }
    if (!currentGroup.lastchange) {
        dispatch(AlertActions.AddAlert({'main': 'Chyba uložení', 'explain': `u ${JSON.stringify(newAction)} není atribut lastchange`, 'type': 'alert-danger'}))
    }

    dispatch(GroupActions.updateGroup(newAction))
    const updateGQL = () => GroupUpdateQuery(newAction)
        .then(response => response.json())
        .then(json => {
            if (json.errors) {
                dispatch(AlertActions.AddAlert({'main': 'Chyba uložení', 'explain': json.errors[0].message, 'type': 'alert-danger'}))
            } else {
                const updateResult = json.data.groupById.editor.update
                const resultStatus = updateResult.result
                const changedGroup = updateResult.group

                if (resultStatus === "ok") {
                    // data byla skutecne ulozena
                    dispatch(AlertActions.AddAlert({'main': 'Ok', 'explain': 'Změny uloženy', 'type': 'alert-success'}))
                    // poznamenat si lastchange pro příští uložení
                    dispatch(GroupActions.updateGroup({...group, 'lastchange': changedGroup.lastchange}))

                } else {
                    // data se nepodarilo ulozit, ale odpoved od serveru doputovala
                    const overwriteFunc = () => {
                        //musime zmenit lastchange in state
                        dispatch(GroupActions.updateGroup({...group, 'lastchange': changedGroup.lastchange}))
                        //retry save
                        dispatch(updateGroupAsync({...group}))
                    }
                    const acceptFunc = () => {
                        //accept server state
                        console.log(changedGroup)
                        console.log(getState())
                        dispatch(GroupActions.updateGroup({...changedGroup}))
                        console.log(getState())
                    }
                    dispatch(AlertActions.AddAlert(
                        {
                            'main': 'Ok', 'explain': 'Někdo na serveru provedl změnu, chcete ji přepsat?', 'type': 'alert-danger', 
                            'extraButtons': [
                                {'props': {'className': 'btn btn-warning'}, 'onClick': overwriteFunc, 'label': 'Vynutit přepsání'},
                                {'props': {'className': 'btn btn-warning'}, 'onClick': acceptFunc, 'label': 'Převzít data ze serveru'}
                            ]
                        }
                    ))                    
                }
            }
            return json
        })
        .catch((e) => dispatch(AlertActions.AddAlert({'main': 'Chyba uložení', 'explain': e, 'type': 'alert-danger'})))

    updateGroupDelayer(updateGQL)
}

export const loadGroupAsync = (group, query=GroupBaseQuery) => (dispatch, getState) => {
    query(group.id)
        .then(response => response.json())
        .then(json => {
            if (json.errors) {
                const e = json.errors[0]
                dispatch(AlertActions.AddAlert({'main': 'Chyba na serveru', 'explain': e.message, 'type': 'alert-danger'}))
            }
            return json
        })
        .then(json => json.data.groupById)
        .then(data => {
            dispatch(GroupActions.setGroup({}));
            dispatch(GroupActions.updateGroup(data));
        })
}

export const extendGroupAsync = (group, query=GroupBaseQuery) => (dispatch, getState) => {
    query(group.id)
        .then(response => response.json())
        .then(json => {
            if (json.errors) {
                const e = json.errors[0]
                dispatch(AlertActions.AddAlert({'main': 'Chyba na serveru', 'explain': e.message, 'type': 'alert-danger'}))
            }
            return json
        })
        .then(json => json.data.groupById)
        .then(data => {
            dispatch(GroupActions.updateGroup(data));
        })
}

export const addRoleAsync = (group, role, user) => (dispatch, getState) => {
    const query = null
    query(group.id)
}

export const loadMemberAsync = (user, query) => (dispatch, getState) => {
    query(user.id)
        .then(response => response.json())
        .then(json => json.data.userById)
        .then(data => {
            (dispatch(GroupActions.updateGroupMember(data)))
        }
    )
}

const updateGroupInTree = (state, action) => {
    const groupToUpdate = findGroupInState(state, action.payload)
    if (groupToUpdate !== undefined) {
        console.log('updateGroupInTree', groupToUpdate)
        console.log('updateGroupInTree', action.payload)
        groupToUpdate.valid = action.payload.valid
        groupToUpdate.name = action.payload.name
        groupToUpdate.lastchange = action.payload.lastchange
    }
}

const updateGroup = (state, action) => {
    //udelat poradek v updates,
    if (state.id === undefined) {
        return ({...state, ...action.payload})
    } else {
        return ({...state, ...action.payload})
    }
    
}

const updateGroupMember = (state, action) => {
    //immer library expected
    const user = action.payload
    const membershipToUpdate = state.memberships?.filter( m => m.user.id === user.id) || {} //warning, action execution can be ignored
    membershipToUpdate.user = {...membershipToUpdate.user, ...user}
}

const setGroup = (state, action) => action.payload
export const GroupSlice = createSlice({
    name: 'group',
    initialState: {},
    reducers: {
        updateGroup,
        setGroup,
        updateGroupMember,
        updateGroupInTree
    }
})

/*
const {
    actions: { updateName },
    reducer: nameReducer
  } = nameSlice;
*/
export const GroupActions = GroupSlice.actions
export const GroupReducer = GroupSlice.reducer