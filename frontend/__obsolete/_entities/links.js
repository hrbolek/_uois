import { Link, useParams } from "react-router-dom";


import { usersPath, groupsPath } from "config/index";

import { root } from "config/index"

export const TeacherSmall = (props) => {
    return (
        <>
        <Link to={root + "/users/teacher/" + (props.id)}>{props.name} {props.surname} </Link>
        <a href={"mailto:" + props.email}><i className="bi bi-envelope"></i></a>
        </>
    )
}

export const StudentSmall = (props) => {
    return (
        <>
        <Link to={root + "/users/student/" + (props.id)}>{props.name} {props.surname} </Link>
        <a href={"mailto:" + props.email}><i className="bi bi-envelope"></i></a>
        </>
    )
}

export const FacultySmall = (props) => {
    return (
        <Link to={root + "/groups/faculty/" + (props.id)}>{props.name}</Link>
    )
}

export const DepartmentSmall = (props) => {
    return (
        <Link to={root + "/groups/department/" + (props.id)}>{props.name}</Link>
    )
}

export const UniversitySmall = (props) => {
    return (
        <Link to={root + "/groups/university/" + (props.id)}>{props.name}</Link>
    )
}

export const StudyGroupSmall = (props) => {
    return (
        <Link to={root + "/groups/studygroup/" + (props.id)}>{props.name}</Link>
    )
}
