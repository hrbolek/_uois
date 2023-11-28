import { useRouteError } from "react-router-dom";
import { UserEventsCard } from "./Cards";
import { UserGeneralPage } from "./Pages";
import { UserClassificationsCard, UserGroupsCard, UserRolesCard } from "./Cards";
// import { UserPage } from "./Pages";

export * from './Actions'
export * from './Cards'
export * from './Components'
export * from './Pages'

function ErrorBoundary() {
    const error = useRouteError();
    console.error(error);
    return <div>{error.message}</div>;
}

export const UserRoutes = (dispatch) => {
    return [
        {
            path: "/users/:id",
            element: <UserGeneralPage Component={UserEventsCard} editable={false} />,
        },
        {
            path: "/users/edit/:id",
            element: <UserGeneralPage Component={UserEventsCard} editable={true} />,
        },
        {
            path: "/users/calendar/:id",
            element: <UserGeneralPage Component={UserEventsCard} editable={false} />,
        },
        {
            path: "/users/calendar/edit/:id",
            element: <UserGeneralPage Component={UserEventsCard} editable={true} />,
        },
        {
            path: "/users/roles/:id",
            element: <UserGeneralPage Component={UserRolesCard} editable={false} />,
        },
        {
            path: "/users/roles/edit/:id",
            element: <UserGeneralPage Component={UserRolesCard} editable={true} />,
        },
        {
            path: "/users/classification/:id",
            element: <UserGeneralPage Component={UserClassificationsCard} editable={false} />,
        },
        {
            path: "/users/classification/edit/:id",
            element: <UserGeneralPage Component={UserClassificationsCard} editable={true} />,
        },
        {
            path: "/users/subgroups/:id",
            element: <UserGeneralPage Component={UserGroupsCard} editable={false} />,
        },
        {
            path: "/users/subgroups/edit/:id",
            element: <UserGeneralPage Component={UserGroupsCard} editable={true} />,
        },
        {
            path: "/users/members/:id",
            element: <UserGeneralPage Component={UserGroupsCard} editable={false} />,
        },
        {
            path: "/users/members/edit/:id",
            element: <UserGeneralPage Component={UserGroupsCard} editable={true} />,
        },
        // {
        //     path: "/users/",
        //     element: <UserGeneralPage editable={false} />,
        //     errorElement: <ErrorBoundary />,
        //     children: [
        //         // {
        //         //     index: true,
        //         //     element: <UserGeneralPage editable={false} />,
        //         // },
        //         {
        //             path: "/users/:id",
        //             element: <UserGeneralPage Component={UserEventsCard} editable={false} />,
        //         },
        //         {
        //             path: "/users/edit/:id",
        //             element: <UserGeneralPage Component={UserEventsCard} editable={true} />,
        //         },
        //         {
        //             path: "/users/calendar/:id",
        //             element: <UserGeneralPage Component={UserEventsCard} editable={false} />,
        //         },
        //         {
        //             path: "/users/calendar/edit/:id",
        //             element: <UserGeneralPage Component={UserEventsCard} editable={true} />,
        //         },
        //         {
        //             path: "/users/roles/:id",
        //             element: <UserGeneralPage Component={UserRolesCard} editable={false} />,
        //         },
        //         {
        //             path: "/users/roles/edit/:id",
        //             element: <UserGeneralPage Component={UserRolesCard} editable={true} />,
        //         },
        //         {
        //             path: "/users/classification/:id",
        //             element: <UserGeneralPage Component={UserClassificationsCard} editable={false} />,
        //         },
        //         {
        //             path: "/users/classification/edit/:id",
        //             element: <UserGeneralPage Component={UserClassificationsCard} editable={true} />,
        //         },
        //         {
        //             path: "/users/subgroups/:id",
        //             element: <UserGeneralPage Component={UserGroupsCard} editable={false} />,
        //         },
        //         {
        //             path: "/users/subgroups/edit/:id",
        //             element: <UserGeneralPage Component={UserGroupsCard} editable={true} />,
        //         },
        //         {
        //             path: "/users/members/:id",
        //             element: <UserGeneralPage Component={UserGroupsCard} editable={false} />,
        //         },
        //         {
        //             path: "/users/members/edit/:id",
        //             element: <UserGeneralPage Component={UserGroupsCard} editable={true} />,
        //         },
        
        //     ]
        // },
        // {
        //     path: "/users/:id",
        //     element: <UserGeneralPage editable={false} />,
        // },
        // {
        //     path: "/users/edit/:id",
        //     element: <UserGeneralPage editable={true} />,
        // },
        // {
        //     path: "/users/calendar/:id",
        //     element: <UserGeneralPage Component={UserEventsCard} editable={false} />,
        // },
        // {
        //     path: "/users/calendar/edit/:id",
        //     element: <UserGeneralPage editable={true} />,
        // },
        // {
        //     path: "/users/subgroups/:id",
        //     element: <UserGeneralPage Component={UserEventsCard} editable={false} />,
        // },
        // {
        //     path: "/users/subgroups/edit/:id",
        //     element: <UserGeneralPage editable={true} />,
        // },
        // {
        //     path: "/users/roles/:id",
        //     element: <UserGeneralPage Component={UserEventsCard} editable={false} />,
        // },
        // {
        //     path: "/users/roles/edit/:id",
        //     element: <UserGeneralPage editable={true} />,
        // },
        // {
        //     path: "/users/classifications/:id",
        //     element: <UserGeneralPage editable={false} />,
        // },
        // {
        //     path: "/users/classifications/edit/:id",
        //     element: <UserGeneralPage editable={true} />,
        // },
    ]
}
