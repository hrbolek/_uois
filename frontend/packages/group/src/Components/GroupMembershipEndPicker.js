import { useDispatch } from "react-redux"
import { GroupMembershipUpdateAsyncAction } from "./GroupMemberRemoveButton"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared";
import { DatePicker }   from "./DatePicker"

/**
 * 
 * @param {*} group  
 * @param {*} membership
 * @returns JSX.Element Button like datetime picker when change is done, it is saved to database
 */
export const GroupMembershipEndPicker = ({group, user=null, membership}) => {
    const dispatch = useDispatch()
    const onDateChange = (value) => {
        if (group) {
            const updatedMembership = {...membership, enddate: value}
            dispatch(GroupMembershipUpdateAsyncAction({group, membership: updatedMembership}))
            .then(
                CheckGQLError({
                    "ok": () => dispatch(MsgFlashAction({title: "Změna ok"})),
                    "fail": (json) => dispatch(MsgAddAction({title: "Změna se nepovedla\n " + JSON.stringify(json)}))
                })
            )
        }
    }
    // const cdate = membership.enddate ? new Date(membership.enddate + 'Z'): null
    return (
        <DatePicker selected={membership.enddate} onChange={onDateChange} />
    )
}