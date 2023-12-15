import { Provider } from "react-redux"

import { configureStore } from "@reduxjs/toolkit"
import { ItemReducer, MsgReducer } from "../.."

export const AppProvider = ({children}) => {
    const store = configureStore({ 
        reducer: {
            items: ItemReducer,
            msgs: MsgReducer
        }, 
        preloadedState: {
            items: {},
            msgs: {}
        }
    })
    
    return (
        <Provider store={store}>{children}</Provider>
    )
}

