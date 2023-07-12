import React from 'react';
import ReactDOM from 'react-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { UGRoutes } from './components/UG';
import { Router, Routes, Route, BrowserRouter  } from 'react-router-dom';
import { UserPage as UP } from 'pages/UserPage';
import { AppProvider } from 'pages/AppProvider';
import { createRoot } from "react-dom/client"
import { Layout } from 'pages/Layout';
import { ApiPage } from './pages/ApiPage';

import { Pages as UserPages } from '@uoisfrontend/user';
import { Pages as GroupPages } from '@uoisfrontend/group';
import { Pages as EventPages } from '@uoisfrontend/event';
import { Pages as FacilityPages } from '@uoisfrontend/facility';
import { Pages as SurveyPages } from '@uoisfrontend/survey';
import { Pages as ProgramPages } from '@uoisfrontend/program';
import { Pages as PlanPages } from '@uoisfrontend/plan';
import { Pages as FormPages } from '@uoisfrontend/form';
import { Pages as SpecialPages } from '@uoisfrontend/special';
import { LoginButton, LoginPage } from '@uoisfrontend/shared';
const App = () => {
    return (
        <AppProvider>
            <Layout>
                <BrowserRouter >
                    <Routes>
                        <Route path={"/ui/api/"} element={<ApiPage />} />
                        <Route path={"/ui/login/"} element={<LoginPage><LoginButton /></LoginPage>} />
                        {UserPages()}
                        {GroupPages()}
                        {EventPages()}
                        {FacilityPages()}
                        {SurveyPages()}
                        {ProgramPages()}
                        {PlanPages()}
                        {FormPages()}
                        {SpecialPages()}  {/* Musi byt posledni */}
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
