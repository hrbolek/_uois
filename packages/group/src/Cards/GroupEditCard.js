import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { EyeFill, PeopleFill } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"
import { GroupSubgroups } from "../Components/GroupSubgroups"
import { GroupRoles } from "../Components/GroupRoles"
import { GroupMembers } from "../Components/GroupMembers"
import { GroupRolesEdit } from "../Components/GroupRolesEdit"
import { GroupMembersEdit } from "../Components/GroupMembersEdit"
import { GroupMemberAddWithSearch } from "../Components/GroupMemberRemoveButton"
import { GroupRoleAddWithSearch } from "../Components/GroupRoleAddWithSearch"
import { GroupAttributesEditable } from "../Components/GroupAttributesEditable"
import { GroupSubgroupsTable } from "../Components/GroupSubgroupsTable"

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

            </Card.Body>
            <Card.Body>
                <GroupSubgroupsTable group={group} />
            </Card.Body>
            <Card.Body>

                <Row>
                    <Col md={6}>
                        <GroupRolesEdit group={group} onlyValid={true} />
                    </Col>
                    <Col md={6}>
                        <GroupRolesEdit group={group} onlyInvalid={true} />
                    </Col>
                </Row>
                <Row>
                    <Col md={12}>
                        <GroupRoleAddWithSearch group={group}/>
                    </Col>
                </Row>

            </Card.Body>
            <Card.Body>
                <Row>
                    <Col md={6}>
                        <GroupMembersEdit group={group} onlyValid={true} />
                    </Col>
                    <Col md={6}>
                        <GroupMembersEdit group={group} onlyInvalid={true} />
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