import { Link, NavLink } from 'react-router-dom'

import { rootPath as root } from 'generals/config'

//className="btn btn-sm btn-outline-info"
const teacherRoot = root + "/users/teacher"

const spanClass = "ms-1 d-none d-sm-inline text-white"


const links = [
    {'path': '/', 'text': ' Home', 'icon': 'bi-house'},
    {'path': '/timetable/', 'text': ' Rozvrh', 'icon': 'bi-calendar-week'},
    {'path': '/tasks/', 'text': ' Úkoly', 'icon': 'bi-card-checklist'},
    {'path': '/requests/', 'text': ' Zprávy', 'icon': 'bi-envelope'},
    {'path': '/groups/', 'text': ' Výuka', 'icon': 'bi-book'},
    {'path': '/supervisor/', 'text': ' Školitel', 'icon': 'bi-people'},
    {'path': '/grant/', 'text': ' Garance', 'icon': 'bi-collection'},
    {'path': '/timetable/', 'text': ' Věda', 'icon': 'bi-award'},
]

//<Route path={`teacher/subjects/:id`} element={<TeacherSubjectsPage />} />
//<Route path={`teacher/requests/:id`} element={<TeacherMessagesPage />} />

export const TeacherMenu = (props) => {
    const id = props.id
    return (
        <ul className="text-white">
            {links.map(
                (item, index) => 
                    <NavLink key={item.text} to={teacherRoot + item.path + (id)} className="nav-link align-middle px-0">
                        <i className={"fs-4 bi " + item.icon}></i> 
                        <span className={spanClass}>{item.text}</span>
                    </NavLink> 
            )}

        </ul>
    )
}

/***
            <NavLink to={teacherRoot + "/" + (id)} className="nav-link align-middle px-0">
                <i className="fs-4 bi bi-house"></i> <span className={spanClass}> Home</span></NavLink> 
            <NavLink to={teacherRoot + "/timetable/" + (id)} className="nav-link align-middle px-0">
                <i className="fs-4 bi bi-calendar-week"></i> <span className={spanClass}> Rozvrh</span></NavLink> 
            <NavLink to={teacherRoot + "/tasks/" + (id)} className="nav-link align-middle px-0">
                <i className="fs-4 bi bi-card-checklist"></i> <span className={spanClass}> Úkoly</span></NavLink> 
            <NavLink to={teacherRoot + "/requests/" + (id)} className="nav-link align-middle px-0">
                <i className="fs-4 bi bi-envelope"></i> <span className={spanClass}> Zprávy</span></NavLink> 
            <NavLink to={teacherRoot + "/groups/" + (id)} className="nav-link align-middle px-0">
                <i className="fs-4 bi bi-book"></i> <span className={spanClass}> Výuka</span></NavLink> 
            <NavLink to={teacherRoot + "/supervisor/" + (id)} className="nav-link align-middle px-0">
                <i className="fs-4 bi bi-people"></i> <span className={spanClass}> Školitel</span></NavLink> 
            <NavLink to={teacherRoot + "/grant/" + (id)} className="nav-link align-middle px-0">
                <i className="fs-4 bi bi-collection"></i> <span className={spanClass}> Garance</span></NavLink> 
            <NavLink to={teacherRoot + "/timetable/" + (id)} className="nav-link align-middle px-0">
                <i className="fs-4 bi bi-award"></i> <span className={spanClass}> Věda</span></NavLink> 

 * 
 */