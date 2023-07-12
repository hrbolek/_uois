import { Route } from "react-router-dom";
import { ProgramPage } from "./Pages/ProgramPage";
import { ProgramEditPage } from "./Pages/ProgramEditPage";
import { SubjectPage } from "./Pages/SubjectPage";
import { SubjectEditPage } from "./Pages/SubjectEditPage";
import { ClassificationUserPage } from "./Pages/ClassificationUserPage";
import { SemesterPage } from "./Pages/SemesterPage";

export * from "./Pages/ProgramPage";
export * from "./Pages/ProgramEditPage";
export * from "./Pages/SubjectPage";
export * from "./Pages/SubjectEditPage";
export * from "./Pages/ClassificationUserPage";

export const Pages = () => {
    return (
        <>
            <Route path={"/ui/programs/edit/:id"} element={<ProgramEditPage />} />
            <Route path={"/ui/programs/:id"} element={<ProgramPage />} />      
            <Route path={"/ui/subjects/edit/:id"} element={<SubjectEditPage />} />
            <Route path={"/ui/subjects/:id"} element={<SubjectPage />} />      

            <Route path={"/ui/semesters/edit/:id"} element={<SemesterPage />} />
            <Route path={"/ui/semesters/:id"} element={<SemesterPage />} />      

            <Route path={"/ui/classification/user/:id"} element={<ClassificationUserPage />} />      
        </>
    )
}

export default Pages