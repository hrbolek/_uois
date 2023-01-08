import { Link } from "react-router-dom";


//import { usersPath, groupsPath } from "config/index";

import { rootPath } from "generals/config"

export const UserSmall = (props) => {
    const { user } = props
    //        <Link to={rootPath + "/users/" + (user.id)}>{user.name} {user.surname} </Link>
    //<a href={rootPath + "/users/" + (user.id)}>{user.name} {user.surname} </a>
    return (
        <>
        <Link to={rootPath + "/users/" + (user.id)}>{user.name} {user.surname} </Link>
        <a href={"mailto:" + user.email}><i className="bi bi-envelope"></i></a>
        </>
    )
}

export const StudentSmall = (props) => {
    const { user } = props
    //        <Link to={rootPath + "/users/student/" + (user.id)}>{user.name} {user.surname} </Link>
    //<a href={rootPath + "/users/student/" + (user.id)}>{user.name} {user.surname} </a>
    return (
        <>
        <Link to={rootPath + "/users/student/" + (user.id)}>{user.name} {user.surname} </Link>
        <a href={"mailto:" + user.email}><i className="bi bi-envelope"></i></a>
        </>
    )
}

