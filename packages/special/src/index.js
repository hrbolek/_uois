import { Route } from "react-router-dom";
import { AdminPage } from "./Pages/AdminPage";
import { HomePage } from "./Pages/HomePage";
import { SearchPage } from "./Pages/SearchPage";

export * from "./Pages/AdminPage";
export * from "./Pages/HomePage";
export * from "./Pages/SearchPage";

export const Pages = () => {
    return (
        <>
            <Route path={"/ui/admin"} element={<AdminPage />} />
            <Route path={"/ui/home"} element={<HomePage />} />      
            <Route path={"/ui"} element={<SearchPage />} />      {/* Musi byt posledni */}
        </>
    )
}

export default Pages