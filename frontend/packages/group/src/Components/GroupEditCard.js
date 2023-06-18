import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { EyeFill, PeopleFill } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"
import { GroupSubgroups } from "./GroupSubgroups"
import { GroupRoles } from "./GroupRoles"
import { GroupMembers } from "./GroupMembers"
import { GroupRolesEdit } from "./GroupRolesEdit"
import { GroupMembersEdit } from "./GroupMembersEdit"
import { GroupMemberAddWithSearch } from "./GroupMemberRemoveButton"
import { GroupRoleAddWithSearch } from "./GroupRoleAddWithSearch"
import { GroupAttributesEditable } from "./GroupAttributesEditable"

export const GroupEditCard = ({group}) => {
    const mastergroup = group?.mastergroup
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <PeopleFill /> {group.name} ({group?.grouptype?.name})
                    </Col>
                    <Col>
                        {
                            mastergroup ? <Link id={mastergroup.id} tag="group">{mastergroup.name}</Link> : ""
                        }
                        
                    </Col>
                    <Col>
                        <GroupRoles group={group} />
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            <Link id={group.id} tag="group"><EyeFill /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            {/* <Card.Body>
                {JSON.stringify(group)}
            </Card.Body> */}
            <Card.Body>
                <GroupAttributesEditable group={group} />
                <Row>
                    <Col md={6}>
                        <GroupRolesEdit group={group} validOnly={true} />
                    </Col>
                    <Col md={6}>
                        <GroupRolesEdit group={group} invalidOnly={true} />
                    </Col>
                </Row>
                <Row>
                    <Col md={12}>
                        <GroupRoleAddWithSearch group={group}/>
                    </Col>
                </Row>
                <Row>
                    <Col md={6}>
                        <GroupMembersEdit group={group} validOnly={true} />
                    </Col>
                    <Col md={6}>
                        <GroupMembersEdit group={group} invalidOnly={true} />
                    </Col>
                </Row>
                <Row>
                    <Col md={12}>
                        <GroupMemberAddWithSearch group={group}/>
                    </Col>
                </Row>
                <Row>
                    <Col md={6}>
                        <GroupSubgroups group={group} />
                    </Col>
                    <Col md={6}>
                        <GroupSubgroups group={group} />
                    </Col>
                </Row>
                {JSON.stringify(group)}
            </Card.Body>
        </Card>
    )
}