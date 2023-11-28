import { Diagram3 } from "react-bootstrap-icons"
import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"
import { GroupRolesCard } from "./GroupRolesCard"
import { GroupSubgroups } from "../Components"

export const GroupSubgroupsCard = ({filter=(g=>true), group}) => {
    const subgroups = group?.subgroups.filter(filter) || []
    
    return (
        <Card>
            <Card.Header>
                <Diagram3 /> Prvky
            </Card.Header>
            <Card.Body>
                <GroupSubgroups group={group} />
            </Card.Body>
        </Card>
    )
}