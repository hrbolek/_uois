import { useFreshItem } from "@uoisfrontend/shared";
import { UserFetchAsyncAction } from "@uoisfrontend/user";

export const UserGet = (props) => {
    const {id, Visualiser} = props   
    const [user] = useFreshItem({id}, UserFetchAsyncAction)
    const newProps = {...props, user}
    if (user) {
        return (
            <Visualiser {...newProps} />
        )
    } else {
        return <>Loading...</>
    }
}

export const UserDecorator = (Story, storyprops) => {
    const id = storyprops?.args?.user?.id
    const [user] = useFreshItem({id}, UserFetchAsyncAction)
    storyprops.args["user"] = {...storyprops.args["user"], ...user}
    // console.log("UserDecorator", storyprops)
    // console.log("UserDecorator", user)
    return (
        <Story {...storyprops} />
    )
}