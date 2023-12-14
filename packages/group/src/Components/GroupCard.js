import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"

import { PencilSquare, PeopleFill } from "react-bootstrap-icons"
import { Link } from "@uoisfrontend/shared"
import { GroupSubgroups } from "./GroupSubgroups"
import { GroupRoles } from "./GroupRoles"
import { GroupMembers } from "./GroupMembers"
import { GroupSearch, GroupSugestionLink } from "./GroupSearch"
import { GroupSchema } from './GroupSchema'

import { GroupClassifications } from './GroupClassifications'


const ShowMembers = (group) => {
    const results = {
        "": true,
        "cd49e152-610c-11ed-9f29-001a7dda7110": false,
        "cd49e154-610c-11ed-bdbf-001a7dda7110": false,
        "cd49e153-610c-11ed-bf19-001a7dda7110": false,
        "cd49e155-610c-11ed-bdbf-001a7dda7110": false,
        "cd49e155-610c-11ed-844e-001a7dda7110": true,
        "cd49e157-610c-11ed-9312-001a7dda7110": true
    }
    const grouptype = group?.grouptype.id || ""
    const result = results[grouptype]// || false
    //console.log("ShowMembers", group.name, group?.grouptype?.id, result)
    return result
}

export const GroupCard = ({group}) => {
    const mastergroup = group?.mastergroup
    const onSelect = (group) => {

    }
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
                        <div className="float-end">
                            <GroupSearch Suggestion={GroupSugestionLink} onSelect={onSelect}/>
                        </div>
                    </Col>
                    <Col md={1}>
                        <div className="d-flex justify-content-end">
                            <Link id={group.id} tag="groupedit"><PencilSquare /> </Link>
                        </div>
                    </Col>
                </Row>

            </Card.Header>
            <Card.Body>
                <Row>
                    <Col>
                        <GroupSchema group={group} />
                    </Col>
                </Row>

                <Row>
                    <Col>
                        <GroupSubgroups group={group} />
                    </Col>
                </Row>
                {ShowMembers(group)?
                    <Row>
                        <Col>
                            <GroupMembers group={group} />
                        </Col>
                    </Row> : ""
                }
                {true?
                    <Row>
                        <Col>
                            <GroupClassifications group={group} />
                        </Col>
                    </Row> : ""
                }
                
                {/* {JSON.stringify(group)} */}
            </Card.Body>
        </Card>
    )
}