import { Link, useParams } from "react-router-dom";


//import { usersPath, groupsPath } from "config/index";

import { rootPath } from "generals/config"

export const TeacherSmall = (props) => {
    const { user } = props
    return (
        <>
        <Link to={rootPath + "/users/teacher/" + (user.id)}>{user.name} {user.surname} </Link>
        <a href={"mailto:" + user.email}><i className="bi bi-envelope"></i></a>
        </>
    )
}

export const StudentSmall = (props) => {
    const { user } = props
    return (
        <>
        <Link to={rootPath + "/users/student/" + (user.id)}>{user.name} {user.surname} </Link>
        <a href={"mailto:" + user.email}><i className="bi bi-envelope"></i></a>
        </>
    )
}

export const FacultySmall = (props) => {
    console.log(rootPath)
    return (
        <Link to={rootPath + "/groups/faculty/" + (props.id)}>{props.name}</Link>
    )
}

export const DepartmentSmall = (props) => {
    return (
        <Link to={rootPath + "/groups/department/" + (props.id)}>{props.name}</Link>
    )
}

export const UniversitySmall = (props) => {
    return (
        <Link to={rootPath + "/groups/university/" + (props.id)}>{props.name}</Link>
    )
}

export const StudyGroupSmall = (props) => {
    return (
        <Link to={rootPath + "/groups/studygroup/" + (props.id)}>{props.name}</Link>
    )
}

export const GroupSmall = (props) => {
    return (
        <Link to={rootPath + "/groups/" + (props.id)}>{props.name}</Link>
    )
}
