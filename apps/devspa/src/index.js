import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';

import React from 'react';
import reportWebVitals from './reportWebVitals';
import { createRoot } from "react-dom/client"
import { AppProvider } from '@uoisfrontend/shared';

const App = () => {
    return (
        <AppProvider>
            <div>Hello</div>
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
