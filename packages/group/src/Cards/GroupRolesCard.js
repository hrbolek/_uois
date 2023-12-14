import Card from "react-bootstrap/Card"
import { Link } from "react-router-dom"
import { GroupRoles } from "../Components"

export const GroupRolesCard = ({group}) => {
    return (
            <Card>
                <Card.Header>
                    <Link to={"../" + group.id} relative="path">{group.name}</Link>
                </Card.Header>
                <Card.Body>
                    <GroupRoles group={group} onlyValid={true} />
                </Card.Body>
            </Card>
    )
}