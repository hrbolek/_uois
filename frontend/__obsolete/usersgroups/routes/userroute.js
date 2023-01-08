import { Route, Outlet, useParams } from "react-router-dom";

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import { TeacherMainPage } from 'usersgroups/pages/TeacherMainPage'
import { TeacherGrantPage } from 'usersgroups/pages/TeacherGrantPage'
import { TeacherMessagesPage } from 'usersgroups/pages/TeacherMessagesPage'
import { TeacherStudyGroupsPage } from 'usersgroups/pages/TeacherStudyGroupsPage'
import { TeacherSubjectsPage } from 'usersgroups/pages/TeacherSubjectsPage'
import { TeacherSupervisorPage } from 'usersgroups/pages/TeacherSupervisorPage'
import { TeacherTasksPage } from 'usersgroups/pages/TeacherTasksPage'
import { TeacherTimeTablePage } from 'usersgroups/pages/TeacherTimeTablePage'
import { UserPage } from 'usersgroups/pages/UserPage'

export const UserRoute = (props) => {
    return (
        <Route path={"users/"} element={<Outlet />}>
            <Route path={`:id`} element={<UserPage />} />
            <Route path={`teacher/:id`} element={<TeacherMainPage />} />
            <Route path={`teacher/:pageType/:id`} element={<TeacherMainPage />} />
        </Route>
    )

/*
            <Route path={`teacher/grant/:id`} element={<TeacherGrantPage />} />
            <Route path={`teacher/timetable/:id`} element={<TeacherTimeTablePage />} />
            <Route path={`teacher/subjects/:id`} element={<TeacherSubjectsPage />} />
            <Route path={`teacher/groups/:id`} element={<TeacherStudyGroupsPage />} />
            <Route path={`teacher/supervisor/:id`} element={<TeacherSupervisorPage />} />
            <Route path={`teacher/tasks/:id`} element={<TeacherTasksPage />} />
            <Route path={`teacher/requests/:id`} element={<TeacherMessagesPage />} />

*/

    /**
            <Route path={`teacher/timetable/:id`} element={<TeacherTimeTablePage />} />
            <Route path={`teacher/grant/:id`} element={<TeacherGrantPage />} />
            <Route path={`teacher/subjects/:id`} element={<TeacherStudyGroupsPage />} />
            <Route path={`teacher/groups/:id`} element={<TeacherStudyGroupsPage />} />
            <Route path={`teacher/supervisor/:id`} element={<TeacherSupervisorPage />} />
            <Route path={`teacher/tasks/:id`} element={<TeacherTasksPage />} />
            <Route path={`teacher/projects/:id`} element={<TeacherTimeTablePage />} />
            <Route path={`teacher/publications/:id`} element={<TeacherTimeTablePage />} />
            <Route path={`teacher/requests/:id`} element={<TeacherMessagesPage />} />

     */
}