import { EditableAttributeText } from "@uoisfrontend/shared"
import { GroupUpdateAsyncAction } from "../Actions/GroupUpdateAsyncAction"

export const GroupNameEditable = ({group}) => {
    return (
        <EditableAttributeText item={group} attributeName={"name"} asyncUpdater={GroupUpdateAsyncAction} label="Název"/>
    )
}