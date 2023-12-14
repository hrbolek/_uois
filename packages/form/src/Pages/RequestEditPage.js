import { useFreshItem } from "@uoisfrontend/shared"
import { useParams } from "react-router-dom"
import { RequestEditCard } from "../Components/RequestEditCard"
import { RequestFetchAsyncAction } from "../Actions/RequestFetchAsyncAction"

export const RequestEditPage = () => {
    const { id } = useParams()
    const [item] = useFreshItem({id}, RequestFetchAsyncAction)

    if (item) {
        return (
            <RequestEditCard request={item} />
        )
    } else {
        return <>Nahrání požadavku id {id}</>
    }
}