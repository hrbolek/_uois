import { GroupMembersFetchAsyncAction } from "@uoisfrontend/group";
import { useFreshItem } from "@uoisfrontend/shared";


export const GroupDecorator = (Story, storyprops) => {
    const id = storyprops?.args?.group?.id
    const [group] = useFreshItem({id}, GroupMembersFetchAsyncAction)
    storyprops.args["group"] = {...storyprops.args["group"], ...group}

    return (
        <Story {...storyprops} />
    )
}