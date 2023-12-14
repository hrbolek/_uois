import { Link } from "@uoisfrontend/shared";
import { PeopleFill } from "react-bootstrap-icons";


export const GroupSubgroup = ({ group, subgroup, children }) => {
    return (
        <>
            <span className="btn btn-outline-success">
                <Link id={subgroup.id} tag="group"><PeopleFill /> {subgroup.name}</Link>
            </span>
            {children}
        </>
    );
};
