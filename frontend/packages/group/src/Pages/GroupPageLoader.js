import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import { Link, json, useLoaderData, useMatch, useMatches, useParams } from 'react-router-dom'
import { Card } from 'react-bootstrap'
import { useState } from 'react'
import { useSelector } from 'react-redux'
import { useFreshItem } from '@uoisfrontend/shared'
import { GroupFetchAsyncAction } from '../Actions'
import { Calendar3, CollectionFill, Diagram3, ListUl, PencilSquare, PeopleFill } from 'react-bootstrap-icons'
import { GroupRoles, GroupSearch } from '../Components'

const LocalLink = ({group}) => {
    return (
        <Link to={"../" + group.grouptype.nameEn + "/" + group.id}>{group.name}</Link>
    )
}

export const GroupPageLoader = ({children}) => {
    
    //const loaderData = useLoaderData()
    const { id } = useParams()
    const [group] = useFreshItem({id}, GroupFetchAsyncAction)
    const mastergroup = group?.mastergroup
    console.log("GroupPageLoader")
    // console.log(JSON.stringify(loaderData))
    console.log(JSON.stringify(group))

    if (!group) {
        return (<>{children}</>)
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
                        mastergroup ? <Link to={"../"+ mastergroup.id} relative="path">{mastergroup.name}</Link> : ""
                    }
                </Col>
                <Col>
                    <GroupRoles group={group} />
                </Col>
                <Col>
                    <div className="float-end">
                        {/* <GroupSearch Suggestion={GroupSugestionLink} onSelect={onSelect}/> */}
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
                <div  style={{width: "3%"}}>
                    <Link to={"../../members/" + group.id} relative='path'><PeopleFill size={32}/></Link> <br />
                    <Link to={"../../subgroups/" + group.id} relative='path'><Diagram3 size={32}/></Link> <br />
                    <Link to={"../../subgroups/" + group.id} relative='path'><Calendar3 size={32}/></Link>
                </div>
                <div  style={{width: "97%"}}>
                    {children}
                </div>
            </Row>
            
        </Card.Body>
        </Card>
    )
}