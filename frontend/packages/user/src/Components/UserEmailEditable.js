import { EditableAttributeText } from "@uoisfrontend/shared"
import { UserUpdateAsyncAction } from "../Actions/UserUpdateAsyncAction"

export const UserEmailEditable = ({user}) => {
    return (
        <EditableAttributeText item={user} attributeName={"email"} asyncUpdater={UserUpdateAsyncAction} />
    )
}
