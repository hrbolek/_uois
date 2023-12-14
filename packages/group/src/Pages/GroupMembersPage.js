import Card from "react-bootstrap/Card"
import Col from "react-bootstrap/Col"
import Row from "react-bootstrap/Row"
import { useParams } from "react-router-dom"

import { useFreshItem } from '@uoisfrontend/shared'
import { GroupMembersFetchAsyncAction } from '../Actions'
import { PeopleFill } from "react-bootstrap-icons"

import { GroupMembersCard } from '../Cards'

export const GroupMembersPage = ({children}) => {
    const {id} = useParams()
    const [group] = useFreshItem({id}, GroupMembersFetchAsyncAction)
    
    return ( <GroupMembersCard group={group} /> )
}