import { Provider } from "react-redux"
import { store, actions } from "../reducers"
import { createContext, useContext, Provider as ReactProvider } from "react"

const ActionsProvider = createContext(actions)
export const AppProvider = ({children}) => {
    return (
        <ActionsProvider.Provider value={actions}>
            <Provider store={store}>
                {children}
            </Provider>
        </ActionsProvider.Provider>
    )
}

export const useActions = () => {
    return useContext(ActionsProvider)
}