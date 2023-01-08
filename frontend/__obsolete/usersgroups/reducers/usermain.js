import { createSlice } from '@reduxjs/toolkit'

import { userUpdateQuery, userLargeQuery } from 'usersgroups/queries/user'
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
    const updateGQL = () => userUpdateQuery(newAction)
        .then(response => response.json())
        .then(json => {
            if (json.errors) {
                dispatch(AlertActions.AddAlert({'main': 'Chyba uložení', 'explain': json.errors[0].message, 'type': 'alert-danger'}))
            } else {
                const changedUser = json.data.userById.editor.update
                let reallyChanged = true
                for (const key in limitedUser) {
                    if (user.hasOwnProperty(key)) {
                          if (user[key] !== changedUser[key]) {
                            reallyChanged = false
                          }
                    }
                }

                if (reallyChanged) {
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

export const loadUserAsync = (user) => (dispatch, getState) => {
    userLargeQuery(user.id)
        .then(response => response.json())
        .then(json => json.data.userById)
        .then(data => {
            (dispatch(UserActions.setUser(data)))
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