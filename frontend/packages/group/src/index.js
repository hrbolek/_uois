import { Route } from "react-router-dom";
import { GroupPage } from "./Pages/GroupPage";
import { GroupEditPage } from "./Pages/GroupEditPage";
import { GroupsPage } from "./Pages/GroupsPage";
import { GroupPageNoUniversity } from './Pages/GroupPageNoUniversity';
import { GroupPageFaculty } from "./Pages/GroupPageFaculty";
import { GroupPageDepartment } from "./Pages/GroupPageDepartment";
import { GroupMembersPage, GroupPageLoader, GroupSubgroupsPage, HelloPage } from "./Pages";
import { Outlet } from "react-bootstrap-icons";
import { GroupFetchAsyncAction, GroupMembersFetchAsyncAction } from "./Actions";
import { IntroductionPage } from "pages/IntroductionPage";
import { GroupGeneralPage } from "./Pages/GroupGeneralPage";
import { GroupCalendarCard, GroupClassificationsCard, GroupMembersCard, GroupMembersEditCard, GroupRolesCard, GroupRolesEditCard, GroupSubgroupsCard } from "./Cards";


export * from './Actions'
export * from './Components'
export * from './Pages'
export * from './Queries'

export const GroupRoutes = (dispatch) => {
    return (
        [
            {
                path: "/groups/:id",
                element: <GroupGeneralPage Component={GroupMembersCard} />,
            },
            {
                path: "/groups/roles/:id",
                element: <GroupGeneralPage Component={GroupRolesCard} />,
            },
            {
                path: "/groups/roles/edit/:id",
                element: <GroupGeneralPage Component={GroupRolesEditCard} />,
            },
            {
                path: "/groups/members/:id",
                element: <GroupGeneralPage Component={GroupMembersCard} AsyncAction={GroupMembersFetchAsyncAction}/>,
            },
            {
                path: "/groups/members/edit/:id",
                element: <GroupGeneralPage Component={GroupMembersEditCard} AsyncAction={GroupMembersFetchAsyncAction}/>,
            },
            {
                path: "/groups/subgroups/:id",
                element: <GroupGeneralPage Component={GroupSubgroupsCard} />,
            },
            {
                path: "/groups/subgroups/edit/:id",
                element: <GroupGeneralPage Component={GroupSubgroupsCard} />,
            },
            {
                path: "/groups/calendar/:id",
                element: <GroupGeneralPage Component={GroupCalendarCard} />,
            },
            {
                path: "/groups/calendar/edit/:id",
                element: <GroupGeneralPage Component={GroupCalendarCard} />,
            },
            {
                path: "/groups/classification/:id",
                element: <GroupGeneralPage Component={GroupClassificationsCard} />,
            },
            {
                path: "/groups/classification/edit/:id",
                element: <GroupGeneralPage Component={GroupClassificationsCard} />,
            },
            // {
            //     path: "/university",
            //     element: <IntroductionPage><Outlet /></IntroductionPage>,
            //     // loader: () => dispatch(GroupFetchAsyncAction({id: "2d9dcd22-a4a2-11ed-b9df-0242ac120003"})),
            //     // id: "university",
            //     children: [
            //     {
            //         path: ":id",
            //         element: <GroupPageLoader reference={"university"}><Outlet /></GroupPageLoader>,
            //         loader: ({params}) => dispatch(GroupFetchAsyncAction({id: params.id})),
            //         id: "university",
            //     },
            //     {
            //         path: "faculty",
            //         element: <GroupPageLoader><Outlet /></GroupPageLoader>,
            //         loader: ({params}) => dispatch(GroupFetchAsyncAction({id: params.id})),
            //         id: "faculties",
            //         children: [
            //         {
            //             path: ":id",
            //             element: <GroupPageLoader reference={"faculty"}><Outlet /></GroupPageLoader>,
            //             loader: ({params}) => dispatch(GroupFetchAsyncAction({id: params.id})),
            //             id: "faculty",
            //         },
            //         {
            //             path: "department/:id",
            //             element: <GroupPageLoader reference={"department"}><Outlet /></GroupPageLoader>,
            //             loader: ({params}) => dispatch(GroupMembersFetchAsyncAction({id: params.id})),
            //             id: "department",
            //         },
            //         ]
            //     },
            //     {
            //         path: "centre/:id",
            //         element: <GroupPageLoader><Outlet /></GroupPageLoader>,
            //         loader: ({params}) => dispatch(GroupFetchAsyncAction({id: params.id})),
            //         id: "centre",
            //     },
            //     ]
            // }
        ]
    )
}


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