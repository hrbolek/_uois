import { Route } from "react-router-dom";
import { ProgramPage } from "./Pages/ProgramPage";
import { ProgramEditPage } from "./Pages/ProgramEditPage";
import { SubjectPage } from "./Pages/SubjectPage";
import { SubjectEditPage } from "./Pages/SubjectEditPage";

export * from "./Pages/ProgramPage";
export * from "./Pages/ProgramEditPage";
export * from "./Pages/SubjectPage";
export * from "./Pages/SubjectEditPage";

export const Pages = () => {
    return (
        <>
            <Route path={"/ui/programs/edit/:id"} element={<ProgramEditPage />} />
            <Route path={"/ui/programs/:id"} element={<ProgramPage />} />      
            <Route path={"/ui/subjects/edit/:id"} element={<SubjectEditPage />} />
            <Route path={"/ui/subjects/:id"} element={<SubjectPage />} />      
        </>
    )
}

export default Pages