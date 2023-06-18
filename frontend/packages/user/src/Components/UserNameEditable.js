import { EditableAttributeText } from "@uoisfrontend/shared"
import { UserUpdateAsyncAction } from "../Actions/UserUpdateAsyncAction"

/**
 * 
 * @param {Object} props.user Object describing an user's entity
 * @returns JSX.Element
 */
export const UserNameEditable = ({user}) => {
    return (
        <EditableAttributeText item={user} attributeName={"name"} asyncUpdater={UserUpdateAsyncAction} />
    )
}
