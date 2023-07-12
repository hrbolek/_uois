import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux/"

import { GroupCard } from "../Components/GroupCard"
import { GroupFetchAsyncAction } from "../Actions/GroupFetchAsyncAction"
import { CheckGQLError, MsgAddAction, MsgFlashAction, useFreshItem } from "@uoisfrontend/shared"
import { GroupMembersFetchAsyncAction } from "../Actions/GroupMembersFetchAsyncAction"
import { Col } from "react-bootstrap"
import { Row } from "react-bootstrap"
import { GroupSearch, GroupSugestionLink } from "../Components/GroupSearch"
import { useMemo } from "react"


export const GroupPageDepartment = () => {
    const dispatch = useDispatch()

    const id = useParams().id
    
    console.log("GroupPage.id", id)
    const [group, updateDone] = useFreshItem({id: id}, 
        GroupMembersFetchAsyncAction)

    updateDone
    // .then(json => json)
    .then(
        CheckGQLError({
            "ok": (json) => dispatch(MsgFlashAction({ title: "Nahrání skupiny úspěšné" })),
            "fail": (json) => dispatch(MsgAddAction({ title: "Chyba " + JSON.stringify(json) })),
        })
    )
    
    
    if (group){        
        return (
            <>
            {/* <Row>
                <Col>
                    <div className="float-end">
                        <GroupSearch Suggestion={GroupSugestionLink} />
                    </div>
                </Col>
            </Row> */}
            <Row>
                <Col>
                    Katedra
                    <GroupCard group={group} />
                </Col>
            </Row>
            
            
            
            </>
        )
    } else {
        return <>Loading group</>
    }
}