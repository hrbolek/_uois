import { createSlice } from '@reduxjs/toolkit';
import { v1 as uuid1 } from 'uuid';

/**
 * Stavova funkce nad dict, pridava prvek
 * @param {*} state 
 * @param {*} action 
 * @returns 
 */
export const CreateItem = (state, action) => {
    const item = action.payload;
    const id = item['id'] || uuid1()
    if (!item['id']) {
        item['id'] = id
    }
    
    state[id] = item
    return state
}

/**
 * Stavova funkce nad dict, maze prvek
 * @param {*} state 
 * @param {*} action 
 * @returns 
 */
export const DeleteItem = (state, action) => {
    const item = action.payload;
    delete state[item.id]

    return state
}

/**
 * Stavova funkce nad dict, dela replace
 * @param {*} state 
 * @param {*} action 
 * @returns 
 */
export const ReplaceItem = (state, action) => {
    const newItem = action.payload;
    state[newItem.id] = newItem

    return state
}

/**
 * Stavova funkce nad dict, dela update
 * @param {*} state 
 * @param {*} action 
 * @returns 
 */
export const UpdateItem = (state, action) => {
    const newItem = action.payload;
    const oldItem = state[newItem.id]
    state[newItem.id] = {...oldItem, ...newItem}
    
    return state
}    

/**
 * Stavova funkce nad dict, pracude s klicem selectedId
 * @param {*} state 
 * @param {*} action 
 * @returns 
 */
export const SelectItem = (state, action) => {
    const item = action.payload
    state.selectedId = item.id

    return state
}

export const ItemUpdateEvents = (state, action) => {
    const {id, events}  = action.payload
    const item = state[id]
    const updatedEvents = {}
    for(let event of item?.events || []) {
        updatedEvents[event.id] = event
    }
    for(let event of events || []) {
        const _ = updatedEvents[event.id] || {}
        updatedEvents[event.id] = {..._, ...event}
    }    
    item.events = Object.values(updatedEvents)
    return state
}

/**
* Kompletni rez budocim store.
* Obsluhuje skupiny
*/
export const ItemSlice = createSlice({
   name: 'items',
   initialState: {},
   reducers: {
       item_add: CreateItem,
       item_delete: DeleteItem,
       item_replace: ReplaceItem,
       item_update: UpdateItem,
       item_update_events: ItemUpdateEvents
   }
})

export const ItemReducer = ItemSlice.reducer
export const ItemActions = ItemSlice.actions