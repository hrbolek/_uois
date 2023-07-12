import { createSlice } from '@reduxjs/toolkit';
import { v1 as uuid1 } from 'uuid';
/**
 * Shared module.
 * @module shared
 */


/**
 * Stavova funkce nad dict, pridava prvek
 * @param {*} state 
 * @param {*} action 
 * @returns updated state
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
 * @returns updated state
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
 * @returns updated state
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
 * @returns updated state
 */
export const UpdateItem = (state, action) => {
    const newItem = action.payload;
    const oldItem = state[newItem.id]
    state[newItem.id] = {...oldItem, ...newItem}
    
    return state
}    

/**
 * Updates an array attribute of item in state if members have __typename attribute, they are added to store
 * @param {*} state 
 * @param {*} action 
 * @returns updated state
 */
export const UpdateSubVector = (state, action) => {
    const { item, vectorname } = action.payload
    const oldItem = state[item.id]
    const subItems = vectorname in oldItem ? oldItem[vectorname] : []
    const indexedSubItems = {}
    for(let i of subItems) {
        indexedSubItems[i.id] = i
    }
    console.log("UpdateSubVector", item)
    console.log("UpdateSubVector", item)
    console.log("UpdateSubVector", item[vectorname])

    
    for(let i of item[vectorname]) {
        if (i?.__typename) {
            //je to polozka, ktera muze byt hlavni, napr. user.events, kazdy event muze byt ve store
            //proved update
            state[i.id] = {...state[i.id], ...i}
        }

        //poznamenej si
        const _ = indexedSubItems[i.id] || {}
        indexedSubItems[i.id] = {..._, ...i}
    }    
    //proved update u hlavni polozky
    oldItem[vectorname] = Object.values(indexedSubItems)
    return state
}

/**
 * Update the scalar attribute of item
 * @param {*} state 
 * @param {} action 
 * @returns updated state
 */
export const UpdateSubScalar = (state, action) => {
    const { item, scalarname } = action.payload
    const oldItem = state[item.id]
    const newSubitem = item[scalarname]
    oldItem[scalarname] = {...oldItem[scalarname], ...newSubitem}
    if (newSubitem?.__typename) {
        //je to polozka, ktera muze byt hlavni, napr. user.events, kazdy event muze byt ve store
        state[newSubitem.id] = {...state[newSubitem.id], ...newSubitem}
    }
    return state
}


const item_add = CreateItem
const item_update = UpdateItem
const item_replace = ReplaceItem
const item_delete = DeleteItem
const item_updateAttributeScalar = UpdateSubScalar
const item_updateAttributeVector = UpdateSubVector


export const ItemSlice = createSlice({
    name: 'items',
    initialState: {},
    reducers: {
        item_add,
        item_update,
        item_replace,
        item_delete,

        item_updateAttributeScalar,
        item_updateAttributeVector,
    } 
})

// export const ItemSlice = createSlice({
//     name: 'items',
//     initialState: {},
//     reducers: {
//         item_add: CreateItem,
//         item_update: UpdateItem,
//         item_replace: ReplaceItem,
//         item_delete: DeleteItem,

//         item_updateAttributeScalar: UpdateSubScalar,
//         item_updateAttributeVector: UpdateSubVector,
//     } 
// })
export const ItemReducer = ItemSlice.reducer
export const ItemActions = ItemSlice.actions

const All = { 
    CreateItem, UpdateItem, ReplaceItem, DeleteItem, 
    UpdateSubVector, UpdateSubScalar, 
    ItemSliceReducer: ItemSlice.reducer, ItemSliceActions: ItemSlice.actions
}
export default All