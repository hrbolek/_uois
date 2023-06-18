import { Route, Outlet } from "react-router-dom";

import { UserPage, UserEditPage } from "pages/UserPage";

export const UGRoutes = (props) => {
    return (
        <Route path={"/ui/users/"} element={<Outlet />}>
            <Route path={"edit/:id"} element={<UserEditPage />} />
            <Route path={`:id`} element={<UserPage />} />
            <Route path={`:pageType/:id`} element={<UserPage />} />
        </Route>
    )
}
