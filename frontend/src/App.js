import './App.css';

import { rootPath as root } from 'generals/config';

import {
  BrowserRouter as Router, Routes, Route,
  Outlet
} from "react-router-dom";

import 'bootstrap/dist/css/bootstrap.min.css';

import { ApiPage } from 'api/pages/api';
//import { DepartmentPage } from './pages/group/department';
//import { FacultyPage } from './pages/group/faculty';

import { UserRoute } from 'users/routes'
import { GroupRoute } from 'groups/routes';

import { IncommingLogin } from 'auth/components/IncommingLogin';
import { SearchPage } from 'search/pages/search';

export function App() {
  /*
  */
    return (
        <Router>
          <Routes>
            <Route path={root + "/api"} element={<ApiPage />}>
            </Route>
            <Route path={root + "/"} element={<Outlet />}>
                {GroupRoute()}
                {UserRoute()}
                <Route path={"login"} element={<IncommingLogin />}>
                </Route>
                <Route path="" element={<SearchPage />}>

                </Route>
            </Route>
           
          </Routes>
      
      </Router>
       );
  }

