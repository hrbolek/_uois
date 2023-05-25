import React from 'react';
import ReactDOM from 'react-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { UGRoutes } from './components/UG';
import { Router, Routes, Route, BrowserRouter  } from 'react-router-dom';
import { UserPage } from 'pages/UserPage';
import { AppProvider } from 'pages/AppProvider';
import { createRoot } from "react-dom/client"
import { Layout } from 'pages/Layout';
import { ApiPage } from './pages/ApiPage';

const App = () => {
    return (
        <AppProvider>
            <Layout>
                <BrowserRouter >
                    <Routes>
                        <Route path={"/ui/api/"} element={<ApiPage />} />
                        {UGRoutes()}
                        {/* <Route path={"/ui/users/:id"} element={<UserPage />} /> */}
                    </Routes>
                </BrowserRouter >
            </Layout>
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
