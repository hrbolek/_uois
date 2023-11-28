import { useRoutes } from "react-router-dom";

const extendRoutes = (routes, params) => {
    const result = routes.map(
        route => extendRoute(route, params)
    )
    return result
}

const extendRoute = (route, params) => {
    const result = {}
    for(const [key, value] in route) {
        if (key === "children") {
            result[key] = extendRoutes(value, params)
            continue
        } 
        if (key === "element") {
            result[key] = {...value, props: {...value.props, ...params}}
            continue
        }
        result[key] = value
    }
    return result
}

export const useCards = (params={}, routes=[]) => {
    const extendedRoutes = extendRoutes(routes)
    return useRoutes(extendedRoutes)
}

// function App() {
//   let element = useRoutes([
//     {
//       path: "/",
//       element: <Dashboard />,
//       children: [
//         {
//           path: "messages",
//           element: <DashboardMessages />,
//         },
//         { path: "tasks", element: <DashboardTasks /> },
//       ],
//     },
//     { path: "team", element: <AboutPage /> },
//   ]);

//   return element;
// }