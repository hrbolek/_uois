import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';

import React from 'react';
import reportWebVitals from './reportWebVitals';
import { createRoot } from "react-dom/client"
import { Provider, useDispatch } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import { ItemReducer } from 'Store';
import { MsgReducer } from 'Store';

import { GroupRoutes } from '@uoisfrontend/group';
import { UserRoutes } from '@uoisfrontend/user';
import { useMemo } from 'react';

const uiroot = "/ui"

const createRouter = (dispatch) => {
    const routes = []
    
    routes.push(...GroupRoutes(dispatch))
    routes.push(...UserRoutes(dispatch))
    
    const router = createBrowserRouter(routes, {basename: uiroot})
    return router
}

const AppRouter = () => {
    console.log("AppRouter")
    const dispatch = useDispatch()
    const router = useMemo(() => createRouter(dispatch), [dispatch])
    //const router = createRouter(dispatch)
    return (
        <RouterProvider router={router} />
    )
}

const AppProvider = ({children}) => {
    console.log("AppProvider")
    const store = configureStore({ 
        reducer: {
            items: ItemReducer,
            msgs: MsgReducer
        }, 
        preloadedState: {
            items: {}
        }
    })
    
    return (
        <Provider store={store}>{children}</Provider>
    )
}



const App = () => {
    return (
        <AppProvider>
            <AppRouter />
        </AppProvider>
    )
}

const container = document.getElementById('root');

// Create a root.
const root = createRoot(container);

// Initial render
root.render(<App />);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
