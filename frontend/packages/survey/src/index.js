import { Route } from "react-router-dom";
import { SurveyPage } from "./Pages/SurveyPage";
import { SurveyEditPage } from "./Pages/SurveyEditPage";
import { SurveyUserPage } from "./Pages/SurveyUserPage";

export * from "./Pages/SurveyPage";
export * from "./Pages/SurveyEditPage";
export * from "./Pages/SurveyUserPage";

export const Pages = () => {
    return (
        <>
            <Route path={"/ui/surveys/edit/:id"} element={<SurveyEditPage />} />
            <Route path={"/ui/surveys/user/:id"} element={<SurveyUserPage />} />
            <Route path={"/ui/surveys/:id"} element={<SurveyPage />} />      
        </>
    )
}

export default Pages