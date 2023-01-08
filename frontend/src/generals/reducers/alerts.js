import { createSlice } from '@reduxjs/toolkit'


//https://stackoverflow.com/questions/105034/how-do-i-create-a-guid-uuid
function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  }

export const AddAlert = (state, action) => { 
    console.log('AddAlert')
    return[...state, {id: uuidv4(), ...action.payload}]
}
export const RemoveAlert = (state, action) => state.filter( item => item.id !== action.payload.id)


export const AlertsSlice = createSlice({
    name: 'alerts',
    initialState: [],
    reducers: {
        AddAlert,
        RemoveAlert
    }
})

export const AlertActions = AlertsSlice.actions
export const AlertsReducer = AlertsSlice.reducer