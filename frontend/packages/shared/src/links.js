import { Link as RouterLink } from "react-router-dom";

export const root = "/ui"
export const linkmap = {
    "user": "/users/",
    "useredit": "/users/edit/",
    "group": "/groups/",
    "groupedit": "/groups/edit/",
    "event": "/events/",
    "eventedit": "/events/edit/",
    "facility": "/facilities/",
    "facilityedit": "/facilities/edit/",
    "project": "/projects/",
    "projectedit": "/projects/edit/",
    
    "survey": "/surveys/",
    "surveyedit": "/surveys/edit/",
    "surveyuser": "/surveys/user/",
    "usersurvey": "/surveys/user/",

    "program": "/programs/",
    "programedit": "/programs/edit/",
    "subject": "/subjects/",
    "subjectedit": "/subjects/edit/",
    "semester": "/semesters/",
    "semesteredit": "/semesters/edit/",

    "classificationuser": "/classification/user/",
    "userclassification": "/classification/user/",

    "plan": "/plans/",
    "planedit": "/plans/edit/",

    "form": "/forms/",
    "formedit": "/forms/edit/",
    "request": "/requests/",
    "requestedit": "/requests/edit/",
}

export const Link = ({id, tag="user", title, children}) => {
    const uri = linkmap[tag] || linkmap["user"]
    return (
        <RouterLink to={root + uri + id}>{title}{children}</RouterLink>
    )
}