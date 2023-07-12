import { Route } from "react-router-dom";
import { GroupPage } from "./Pages/GroupPage";
import { GroupEditPage } from "./Pages/GroupEditPage";
import { GroupsPage } from "./Pages/GroupsPage";
import { GroupPageNoUniversity } from './Pages/GroupPageNoUniversity';
import { GroupPageFaculty } from "./Pages/GroupPageFaculty";
import { GroupPageDepartment } from "./Pages/GroupPageDepartment";

export { GroupFetchAsyncAction } from "./Actions/GroupFetchAsyncAction"; 
export { GroupMembersFetchAsyncAction } from "./Actions/GroupMembersFetchAsyncAction"; 

export { GroupCard } from "./Components/GroupCard";
export { GroupSearch } from "./Components/GroupSearch";
export { GroupRoles } from "./Components/GroupRoles";
export { GroupRolesEdit } from "./Components/GroupRolesEdit";

export { GroupPage } from "./Pages/GroupPage";
export { GroupEditPage } from "./Pages/GroupEditPage";
export { GroupsPage } from "./Pages/GroupsPage";

export const Pages = () => {
    return (
        <>
            <Route path={"/ui/faculty/:id"} element={<GroupPageFaculty />} />
            <Route path={"/ui/department/:id"} element={<GroupPageDepartment />} />
            <Route path={"/ui/groups/nouni/:id"} element={<GroupPageNoUniversity />} />
            <Route path={"/ui/groups/edit/:id"} element={<GroupEditPage />} />
            <Route path={"/ui/groups/:id"} element={<GroupPage />} />
            <Route path={"/ui/groups"} element={<GroupsPage />} />
        </>
    )
}

export default Pages