import { Link, useParams } from "react-router-dom"
import { useDispatch } from "react-redux/"

import { UserCard } from "../Components/UserCard"
import { UserFetchAsyncAction } from "../Actions"
import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { Card, Col, Row } from "react-bootstrap"
import { UserGroups, UserRoles } from "../.."
import { Calendar3, Diagram3, Icon1SquareFill, PencilSquare, PersonFill } from "react-bootstrap-icons"

export const UserPage = ({children, editable=false}) => {
    const dispatch = useDispatch()

    const { id } = useParams()
    const [user, userPromise] = useFreshItem({id}, UserFetchAsyncAction)
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
                    <div  style={{width: "3%"}}>
                        <Link to={"../../classifications/" + user.id} relative='path'><Icon1SquareFill size={32}/></Link> <br />
                        <Link to={"../../groups/" + user.id} relative='path'><Diagram3 size={32}/></Link> <br />
                        <Link to={"../../subgroups/" + user.id} relative='path'><Calendar3 size={32}/></Link>
                    </div>
                    <div  style={{width: "97%"}}>
                        {children?children : <UserCard user={user} />}
                    </div>
                </Row>               
            </Card.Body>
        </Card>
        )
    } else {
        return <>Loading user...</>
    }
}