import { useDispatch } from "react-redux"
import { GroupMembershipUpdateAsyncAction } from "./GroupMemberRemoveButton"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared";
import { DatePicker }   from "./DatePicker"

export const GroupMembershipSetStartPicker = ({group, user=null, membership}) => {
    const dispatch = useDispatch()
    const onDateChange = (value) => {
        if (group) {
            // const iso = value.toISOString().replace('Z', '')
            const updatedMembership = {...membership, startdate: value}
            dispatch(GroupMembershipUpdateAsyncAction({group, membership: updatedMembership}))
            .then(
                CheckGQLError({
                    "ok": () => dispatch(MsgFlashAction({title: "Změna ok"})),
                    "fail": (json) => dispatch(MsgAddAction({title: "Změna se nepovedla\n " + JSON.stringify(json)}))
                })
            )
        }
    }
    // console.log("GroupMembershipSetStartPicker", membership)
    // console.log("GroupMembershipSetStartPicker", membership.startdate)
    return (
        <DatePicker selected={membership.startdate} onChange={onDateChange} />
    )
}