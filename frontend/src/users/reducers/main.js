import { createSlice } from '@reduxjs/toolkit'

import { userUpdateQuery, userLargeQuery } from 'users/queries/user'
import { AlertActions } from 'generals/reducers/alerts';
export const CreateDelayer = (delay=300) => {
    //lokalni promenna
    let oldTimer = -1;
    let state = 0;

    //navratovou hodnotou je funkce umoznujici zpozdeni volani
    return (delayedFunc, callback = () => null) => {

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

const updateUserDelayer = CreateDelayer()
export const updateUserAsync = (user) => (dispatch, getState) => {
    const state = getState()
    //console.log(JSON.stringify(state))
    const currentUser = state.user
    const limitedUser = {name: currentUser.name, surname: currentUser.surname, email: currentUser.email}
    const newAction = {lastchange: currentUser.lastchange, ...limitedUser, ...user}
    
    dispatch(UserActions.updateUser(newAction))
    console.log('going to update on server')
    const updateGQL = () => userUpdateQuery(newAction)
        .then(response => response.json())
        .then(json => {
            if (json.errors) {
                dispatch(AlertActions.AddAlert({'main': 'Chyba uložení', 'explain': json.errors[0].message, 'type': 'alert-danger'}))
            } else {
                const updateResult = json.data.userById.editor.update 
                const changedUser = updateResult.user
                const resultStatus = updateResult.result

                if (resultStatus === "ok") {
                    // data byla skutecne ulozena
                    dispatch(AlertActions.AddAlert({'main': 'Ok', 'explain': 'Změny uloženy', 'type': 'alert-success'}))
                    // poznamenat si lastchange pro příští uložení
                    dispatch(UserActions.updateUser({'lastchange': changedUser.lastchange}))

                } else {
                    // data se nepodarilo ulozit, ale odpoved od serveru doputovala
                    const overwriteFunc = () => {
                        //musime zmenit lastchange in state
                        dispatch(UserActions.updateUser({'lastchange': changedUser.lastchange}))
                        //retry save
                        dispatch(updateUserAsync({...user}))
                    }
                    const acceptFunc = () => {
                        //accept server state
                        console.log(changedUser)
                        console.log(getState())
                        dispatch(UserActions.updateUser({...changedUser}))
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

    updateUserDelayer(updateGQL)
}

//some notes fo async future development
export const convertQueryIntoAsyncAction = (query1) => (payload, query=query1) => 
    (dispatch, getState) => query(payload.id).then(response => response.json())
export const extendAsyncActionWithThen = (asyncAction, thenCallback) => 
    (dispatch, getState) => asyncAction(dispatch, getState).then(thenCallback)

export const encapsulateAsyncAction = (asyncAction, followUpAction) => async (dispatch, getState) => {
    const resultA = await asyncAction(dispatch, getState)
    const resultB = await followUpAction(dispatch, getState, resultA)
    return resultB
}

export const loadUserAsync2 = convertQueryIntoAsyncAction(userLargeQuery)
//end of experiments

export const loadUserAsync = (user, query=userLargeQuery) => (dispatch, getState) => {
    return query(user.id)
        .then(response => response.json())
        .then(json => {
            if (json.errors) {
                const e = json.errors[0]
                dispatch(AlertActions.AddAlert({'main': 'Chyba', 'explain': e.message, 'type': 'alert-danger'}))
                //dispatch(loadUserAsync(user)) // docela prasarna
            }
            return json
        })
        .then(json => json.data.userById)
        .then(data => {
            if (data) {
                dispatch(UserActions.setUser({}))
                dispatch(UserActions.setUser(data))
            } else {
                dispatch(AlertActions.AddAlert({'main': 'Chyba', 'explain': `Uživatel nenalezen (${user.id})`, 'type': 'alert-danger'}))
            }
        }
    )
}

const updateUser = (state, action) => ({...state, ...action.payload})
const setUser = (state, action) => action.payload
export const UserSlice = createSlice({
    name: 'user',
    initialState: {},
    reducers: {
        updateUser,
        setUser
    }
})

/*
const {
    actions: { updateName },
    reducer: nameReducer
  } = nameSlice;
*/
export const UserActions = UserSlice.actions
export const UserReducer = UserSlice.reducer