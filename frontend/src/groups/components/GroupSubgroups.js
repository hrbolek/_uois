import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { GroupSmall } from "groups/components/links"
import { GroupMedium } from "groups/components/GroupMedium"

const Subgroup = (props) => {
    return (
        <Col><GroupMedium group={props.group}/></Col>
    )
}

export const GroupSubgroups = (props) => {
    const { group, grouptype, valid, title } = props
    let subgroups = group.subgroups || []
    if (grouptype) {
        subgroups = subgroups.filter(s => s.grouptype.id === grouptype) || []
    }
    
    subgroups = subgroups.filter(s => s.valid === valid)
    
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    <GroupSmall group={group} /> {title||""}
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <Row>
                    {subgroups.map(
                        group => <Subgroup key={group.id} group={group}/>
                    )
                    }
                </Row>
            </Card.Body>
        </Card>
    )
}