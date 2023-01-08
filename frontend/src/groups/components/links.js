import { Link, useParams } from "react-router-dom";


//import { usersPath, groupsPath } from "config/index";

import { rootPath } from "generals/config"

export const GroupSmall = (props) => {
    const { group } = props
    //<Link to={rootPath + "/groups/" + (group.id)}>{group.name} </Link>
    //<a href={rootPath + "/groups/" + (group.id)}>{group.name} </a>
    return (
        
        <Link to={rootPath + "/groups/" + (group.id)}>{group.name} </Link>
    )
}


