import {
    BrowserRouter as Router, Routes, Route,
    Outlet, Link, useMatch
  } from "react-router-dom";

import { TeacherPage, TeacherTimeTablePage, TeacherSupervisorPage, TeacherTasksPage, TeacherGrantPage, TeacherStudyGroupsPage, TeacherMessagesPage } from './teacher';


export const UserRoute = (props) => {
    return (
        <Route path={"users/"} element={<Outlet />}>
            <Route path={`teacher/:id`} element={<TeacherPage />} />
            <Route path={`teacher/timetable/:id`} element={<TeacherTimeTablePage />} />
            <Route path={`teacher/grant/:id`} element={<TeacherGrantPage />} />
            <Route path={`teacher/subjects/:id`} element={<TeacherStudyGroupsPage />} />
            <Route path={`teacher/groups/:id`} element={<TeacherStudyGroupsPage />} />
            <Route path={`teacher/supervisor/:id`} element={<TeacherSupervisorPage />} />
            <Route path={`teacher/tasks/:id`} element={<TeacherTasksPage />} />
            <Route path={`teacher/projects/:id`} element={<TeacherTimeTablePage />} />
            <Route path={`teacher/publications/:id`} element={<TeacherTimeTablePage />} />
            <Route path={`teacher/requests/:id`} element={<TeacherMessagesPage />} />
        </Route>
    )
}