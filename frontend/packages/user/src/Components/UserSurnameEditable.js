import { EditableAttributeText } from "@uoisfrontend/shared"
import { UserUpdateAsyncAction } from "../Actions/UserUpdateAsyncAction"

export const UserSurnameEditable = ({user}) => {
    return (
        <EditableAttributeText item={user} attributeName={"surname"} asyncUpdater={UserUpdateAsyncAction} />
    )
}
