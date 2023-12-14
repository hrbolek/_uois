import { Link, useParams } from "react-router-dom"
import { useDispatch } from "react-redux/"

import { UserCard } from "../Components/UserCard"
import { UserFetchAsyncAction } from "../Actions"
import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { Card, Col, Row } from "react-bootstrap"
import { UserGroups, UserRoles } from "../.."
import { Calendar3, Diagram3, FlagFill, MortarboardFill, PencilSquare, PeopleFill, PersonFill } from "react-bootstrap-icons"

const resolveChildren = (children=null, Component=null, props={}) => {
    return (children?children: <Component {...props} />)
}

export const UserGeneralPage = ({children, editable=false, Component=UserCard, AsyncAction=UserFetchAsyncAction}) => {
    const dispatch = useDispatch()

    const { id } = useParams()
    const [user, userPromise] = useFreshItem({id}, AsyncAction)
    userPromise.then(
        CheckGQLError({
            "ok": (json) => dispatch(MsgFlashAction({title: "Nahrání uživatele úspěšné"})),
            "fail": (json) => dispatch(MsgAddAction({title: "Chyba " + JSON.stringify(json)})),
        })
    )

    if (user){        
        return (
            <Card>
            <Card.Header>
                <Row>
                    <Col>
                        <PersonFill /> {user.name} {user.surname}  
                        {/* <UserEmail user={user} /> */}
                    </Col>
                    <Col>
                        <UserRoles user={user} />
                    </Col>
                    <Col>
                        <UserGroups user={user} />
                    </Col>
                    <Col>
                        <div className="d-flex justify-content-end">
                            {editable
                                ?<Link to={"../" + user.id} relative="path"><PencilSquare /> </Link>
                                :<Link to={"../edit/" + user.id} relative="path"><PencilSquare /> </Link>
                            }
                        </div>
                    </Col>
                </Row>
            </Card.Header>
            <Card.Body>

            <Row>
                <Col xs={12} sm={12} md={1} style={{border: 0, padding: 0}} className="text-center">
                    <Row>
                        <Col xs={3} sm={3} md={12} style={{}}>
                            <span className='btn btn-outline-primary'><Link to={"/users/roles/" + user.id} relative='path'><FlagFill size={48}/></Link></span>
                        </Col>
                        <Col xs={3} sm={3} md={12} style={{}}>
                            <span className='btn btn-outline-primary'><Link to={"/users/subgroups/" + user.id} relative='path'><Diagram3 size={48}/></Link></span>
                        </Col>
                        <Col xs={3} sm={3} md={12} style={{}}>
                            <span className='btn btn-outline-primary'><Link to={"/users/members/" + user.id} relative='path'><PeopleFill size={48}/></Link></span>
                        </Col>
                        <Col xs={3} sm={3} md={12} style={{}}>
                            <span className='btn btn-outline-primary'><Link to={"/users/calendar/" + user.id} relative='path'><Calendar3 size={48}/></Link></span>
                        </Col>
                        <Col xs={3} sm={3} md={12} style={{}}>
                            <span className='btn btn-outline-primary'><Link to={"/users/classification/" + user.id} relative='path'><MortarboardFill size={48}/></Link></span>
                        </Col>
                    </Row>
                </Col>
                <Col xs={12} sm={12} md={11} >
                    {resolveChildren(children, Component, {user})}
                </Col>
            </Row>

            {/* <Row>
                <div  style={{width: "3%"}}>
                    <Link to={"../classifications/" + user.id} relative='path'><Icon1SquareFill size={32}/></Link> <br />
                    <Link to={"../groups/" + user.id} relative='path'><Diagram3 size={32}/></Link> <br />
                    <Link to={"../calendar/" + user.id} relative='path'><Calendar3 size={32}/></Link>
                </div>
                <div  style={{width: "97%"}}>
                    {children?children : <Component user={user} />}
                </div>
            </Row> */}
                
                
            </Card.Body>
        </Card>

            
        )
    } else {
        return <>Loading user...</>
    }
}