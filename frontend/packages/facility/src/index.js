import { Route } from "react-router-dom";
import { FacilityPage } from "./Pages/FacilityPage";
import { FacilityEditPage } from "./Pages/FacilityEditPage";

export { FacilityPage } from "./Pages/FacilityPage";
export { FacilityEditPage } from "./Pages/FacilityEditPage";
export { FacilitySearch } from './Components/FacilitySearch';

export const Pages = () => {
    return (
        <>
            <Route path={"/ui/facilities/edit/:id"} element={<FacilityEditPage />} />
            <Route path={"/ui/facilities/:id"} element={<FacilityPage />} />      
        </>
    )
}

export default Pages