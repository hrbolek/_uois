import { useDispatch } from "react-redux"
import { CheckGQLError, MsgAddAction, MsgFlashAction } from "@uoisfrontend/shared";
import { DatePicker }   from "./DatePicker"
import { GroupRoleUpdateAsyncAction } from "./GroupRoleValidButton";

export const GroupRoleEndPicker = ({group, user=null, role}) => {
    const dispatch = useDispatch()
    const onDateChange = (value) => {
        if (group) {
            // const iso = value.toISOString().replace('Z', '')
            const updatedRole = {...role, enddate: value}
            dispatch(GroupRoleUpdateAsyncAction({group, role: updatedRole}))
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
        <DatePicker selected={role.enddate} onChange={onDateChange} />
    )
}