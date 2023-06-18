import { configureStore } from "@reduxjs/toolkit"

import { ItemActions, ItemReducer } from "./keyedreducers"
import { MsgActions, MsgReducer} from "./msgs"

/**
 * Toto je hlavni store pro celou aplikaci. Zde zacleneno pro demonstraci. 
 */
const store = configureStore(
    { 
        reducer: {
            items: ItemReducer,
            msgs: MsgReducer
        }, 
        preloadedState: {
            items: {}
        }
})

const dispatch = store.dispatch
export { ItemActions, MsgActions, dispatch, store }