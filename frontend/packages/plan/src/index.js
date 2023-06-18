import { Route } from "react-router-dom";

import { PlanPage } from "./Pages/PlanPage";
import { PlanEditPage } from "./Pages/PlanEditPage";

export * from "./Pages/PlanPage";
export * from "./Pages/PlanEditPage";

export const Pages = () => {
    return (
        <>
            <Route path={"/ui/facilities/edit/:id"} element={<PlanEditPage />} />
            <Route path={"/ui/facilities/:id"} element={<PlanPage />} />      
        </>
    )
}

export default Pages