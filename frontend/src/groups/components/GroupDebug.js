import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { GroupMembers } from 'groups/components/GroupMembers'
import { GroupRoles } from 'groups/components/GroupRoles'
import { GroupSubgroups } from 'groups/components/GroupSubgroups'
import { GroupSchema } from 'groups/components/GroupSchema'
import { GroupSubgroupsEditable } from 'groups/components/GroupSubgroupsEditable'
import { StudentGroupEventList } from 'events/components/StudentGroupEventList'

import { SVGTimeTableG } from 'events/components/SheetA4TimeTable'

export const GroupDebug = (props) => {
    //console.log(props.group)
    //console.log('GroupDebug', Object.keys(props.actions))
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    GroupDebug
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <SVGTimeTableG {...props} /> <br />
            </Card.Body>
            <Card.Body>
                <StudentGroupEventList {...props} /> <br />
                <GroupRoles {...props} /> <br />
                <GroupSchema {...props} /> <br />
                <GroupSubgroupsEditable {...props} /> <br />
                <GroupMembers {...props} /> <br />
            </Card.Body>
        </Card>
    )
}

/**
                <GroupSubgroups {...props} title="fakulty" valid="true" grouptype="cd49e153-610c-11ed-bf19-001a7dda7110"/> <br />
                <GroupSubgroups {...props} title="ústavy" valid="true" grouptype="cd49e154-610c-11ed-bdbf-001a7dda7110"/> <br />
                <GroupSubgroups {...props} title="centra" valid="true" grouptype="cd49e155-610c-11ed-bdbf-001a7dda7110"/> <br />

 */