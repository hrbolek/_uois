import { Route } from "react-router-dom";
import { UserPage } from "./Pages/UserPage";
import { UserEditPage } from "./Pages/UserEditPage";

export { UserPageS } from "./Pages/UserPageS";
export { UserPage } from "./Pages/UserPage";
export { UserEditPage } from "./Pages/UserEditPage";
export { UserSearch } from "./Components/UserSearch";
export { UserClassificationFetchAsyncAction } from "./Actions/UserClassificationFetchAsyncAction"
export { UserClassificationInsertAsyncAction } from "./Actions/UserClassificationInsertAsyncAction"
export { UserFetchAsyncAction } from "./Actions/UserFetchAsyncAction"
export { UserNameEditable } from "./Components/UserNameEditable"
export { UserAttributesEditable } from "./Components/UserAttributesEditable"
export { UserRoles } from "./Components/UserRoles"
export { UserGroups } from "./Components/UserGroups"
export { UserCard } from "./Components/UserCard";
//import "./Pages/UserPageS";


export const Pages = () => {
    return (
        <>
            <Route path={"/ui/users/edit/:id"} element={<UserEditPage />} />
            <Route path={"/ui/users/:id"} element={<UserPage />} />
        </>
    )
}

export default Pages