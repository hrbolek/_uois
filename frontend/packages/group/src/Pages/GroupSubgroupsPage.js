import { useParams, Link } from "react-router-dom"

import { useFreshItem } from '@uoisfrontend/shared'
import { GroupMembersFetchAsyncAction } from '../Actions'
import { GroupSubgroupsCard } from "../Cards"


export const GroupSubgroupsPage = ({filter=(g=>true),children}) => {
    const {id} = useParams()
    const [group] = useFreshItem({id}, GroupMembersFetchAsyncAction)

    if (!group) {
        return children
    }
    
    return (
        <GroupSubgroupsCard group={group} />
    )
}