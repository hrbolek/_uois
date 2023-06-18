import { Route } from "react-router-dom";
import { FormPage } from "./Pages/FormPage";
import { FormEditPage } from "./Pages/FormEditPage";
import { RequestEditPage } from "./Pages/RequestEditPage";

export * from "./Pages/FormPage";
export * from "./Pages/FormEditPage";

export const Pages = () => {
    return (
        <>
            <Route path={"/ui/forms/edit/:id"} element={<FormEditPage />} />
            <Route path={"/ui/forms/:id"} element={<FormPage />} />      

            <Route path={"/ui/requests/edit/:id"} element={<RequestEditPage />} />
            <Route path={"/ui/requests/:id"} element={<RequestEditPage />} />      
        </>
    )
}

export default Pages