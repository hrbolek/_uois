import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import { Link, json, useLoaderData, useLocation, useMatch, useMatches, useParams } from 'react-router-dom'
import { Card } from 'react-bootstrap'
import { useState } from 'react'
import { useSelector } from 'react-redux'
import { useFreshItem, usePath } from '@uoisfrontend/shared'
import { GroupFetchAsyncAction } from '../Actions'
import { Calendar3, Diagram3, EyeFill, FlagFill, MortarboardFill, PencilSquare, People, PeopleFill, PersonFill } from 'react-bootstrap-icons'
import { GroupRoles } from '../Components'
import { GroupSubgroupsCard } from '../Cards'

const LocalLink = ({group}) => {
    return (
        <Link to={"../" + group.grouptype.nameEn + "/" + group.id}>{group.name}</Link>
    )
}

const resolveChildren = (children=null, Component=null, props={}) => {
    return (children?children: <Component {...props} />)
}

export const GroupGeneralPage = ({children, editable=false, AsyncAction=GroupFetchAsyncAction, Component=GroupSubgroupsCard}) => {
    
    // console.log("GroupPageLoader")
    // const match = useMatch("groups/members/edit/:id")
    // console.log("GroupPageLoader.match: ", match)
    // const match2 = useMatch("members/edit/:id")
    // console.log("GroupPageLoader.match: ", match2)
    // const match3 = useMatch("edit/:id")
    // console.log("GroupPageLoader.match: ", match3)
    const {
        editlink: toggleEditUrl, 
        editting,
        linkto
    } = usePath()
    const location = useLocation()
    console.log("GroupPageLoader.match: ", location)

    const matches = useMatches()
    console.log("GroupPageLoader.match: ", matches)

    const { id } = useParams()
    const [group] = useFreshItem({id}, AsyncAction)
    const mastergroup = group?.mastergroup
    
    // console.log(JSON.stringify(loaderData))
    // console.log(JSON.stringify(group))

    if (!group) {
        return (<>Loading !!!</>)
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
                        <Link to={toggleEditUrl}>{editting?<EyeFill />:<PencilSquare />}</Link>
                    </div>
                </Col>
            </Row>

        </Card.Header>
        <Card.Body>
            <Row>
                <Col xs={12} sm={12} md={1} style={{border: 0, padding: 0}} className="text-center">
                    <Row>
                        <Col xs={3} sm={3} md={12} style={{}}>
                            <span className='btn btn-outline-primary'><Link to={"/groups/roles/" + group.id} relative='path'><FlagFill size={48}/></Link></span>
                        </Col>
                        <Col xs={3} sm={3} md={12} style={{}}>
                            <span className='btn btn-outline-primary'><Link to={"/groups/subgroups/" + group.id} relative='path'><Diagram3 size={48}/></Link></span>
                        </Col>
                        <Col xs={3} sm={3} md={12} style={{}}>
                            <span className='btn btn-outline-primary'><Link to={"/groups/members/" + group.id} relative='path'><PeopleFill size={48}/></Link></span>
                        </Col>
                        <Col xs={3} sm={3} md={12} style={{}}>
                            <span className='btn btn-outline-primary'><Link to={"/groups/calendar/" + group.id} relative='path'><Calendar3 size={48}/></Link></span>
                        </Col>
                        <Col xs={3} sm={3} md={12} style={{}}>
                            <span className='btn btn-outline-primary'><Link to={"/groups/classification/" + group.id} relative='path'><MortarboardFill size={48}/></Link></span>
                        </Col>
                    </Row>
                </Col>
                <Col xs={12} sm={12} md={11} >
                    {resolveChildren(children, Component, {group})}
                </Col>
                {/* <div  style={{width: "4%", border: 0, padding: 0}}>
                    <span className='btn btn-outline-primary'><Link to={"/groups/roles/" + group.id} relative='path'><FlagFill /></Link></span> <br />
                    <span className='btn btn-outline-primary'><Link to={"/groups/members/" + group.id} relative='path'><PeopleFill /></Link></span> <br />
                    <span className='btn btn-outline-primary'><Link to={"/groups/subgroups/" + group.id} relative='path'><Diagram3 /></Link></span> <br />
                    <span className='btn btn-outline-primary'><Link to={"/groups/subgroups/" + group.id} relative='path'><Calendar3 /></Link></span>
                    
                    <span className='btn btn-outline-primary'><Link to={"/groups/roles/" + group.id} relative='path'><FlagFill size={48}/></Link></span> <br />
                    <span className='btn btn-outline-primary'><Link to={"/groups/members/" + group.id} relative='path'><PeopleFill size={48}/></Link></span> <br />
                    <span className='btn btn-outline-primary'><Link to={"/groups/subgroups/" + group.id} relative='path'><Diagram3 size={48}/></Link></span> <br />
                    <span className='btn btn-outline-primary'><Link to={"/groups/subgroups/" + group.id} relative='path'><Calendar3 size={48}/></Link></span> 
                </div>
                <div  style={{width: "96%", border: 0, padding: 0}}>
                    {resolveChildren(children, Component, {group})}
                </div> */}
            </Row>
            
        </Card.Body>
        </Card>
    )
}