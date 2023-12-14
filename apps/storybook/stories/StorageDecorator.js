import { store } from "@uoisfrontend/shared";
import { Provider } from "react-redux";

export const StorageDecorator = (Story, storyprops) => {
    // console.log("StorageDecorator", storyprops)
    // storyprops.args["inject"] = "injected"
    // storyprops.args.user["inject"] = "injected"
    return (
        <Provider store={store}>
            <Story {...storyprops} />
        </Provider>
    )
}