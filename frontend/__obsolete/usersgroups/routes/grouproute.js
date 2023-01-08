import { Route, Outlet } from "react-router-dom";

import { GroupPage } from 'usersgroups/pages/GroupPage'

export const GroupRoute = (props) => {
    return (
        <Route path={"groups/"} element={<Outlet />}>
            <Route path={`:pageType/:id`} element={<GroupPage />} />
            <Route path={`:id`} element={<GroupPage />} />
        </Route>
    )
}