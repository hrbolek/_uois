import { DeleteButton } from "@uoisfrontend/shared"
import { PlusLg, TrashFill } from "react-bootstrap-icons"
import { useDispatch } from "react-redux"
import { GroupMembershipUpdateAsyncAction, GroupMembershipUpdateQuery } from "./GroupMemberRemoveButton"



export const GroupMemberValidButton = ({group, membership}) => {
    const dispatch = useDispatch()
    const onChange = (value) => {
        const newMembership = {
            ...membership,
            valid: !membership.valid
        }
        dispatch(GroupMembershipUpdateAsyncAction({group, membership: newMembership}))
        .then(
            json => json
        )
    }
    if (membership?.valid) {
        return (
            <DeleteButton onClick={onChange}><TrashFill /></DeleteButton>
        )    
    } else {
        return (
            <DeleteButton onClick={onChange}><PlusLg /></DeleteButton>
        )
    }
}

