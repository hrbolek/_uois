import Card from "react-bootstrap/Card";
import { Link as RouterLink} from "react-router-dom";

const root = "/ui/"
const urls = {
    user: "users/",
    useredit: "users/edit/",

    group: "groups/",
    groupedit: "groups/edit/"
}

export const Link = ({tag, id, children}) =>  {
    const destination = urls[tag]
    return <RouterLink to={root+destination+id}>{children}</RouterLink>
}
