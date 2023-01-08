import { Route, Outlet } from "react-router-dom";

import { UserPage } from 'users/pages/UserPage';

export const UserRoute = (props) => {
    return (
        <Route path={"users/"} element={<Outlet />}>
            <Route path={`:id`} element={<UserPage />} />
            <Route path={`:pageType/:id`} element={<UserPage />} />
        </Route>
    )
}