import { Link } from "@uoisfrontend/shared"
import { Person, PersonFill } from "react-bootstrap-icons"

export const GroupMember = ({group, membership, children}) => {
    const user = membership?.user
    if (user) {
        return (
            <>  
                <span className="btn btn-outline-success">
                    <Link id={user.id} tag="user"><PersonFill /> {user.name} {user.surname}</Link>
                </span>
                {children}
            </>
        )
    
    } else {
        return <></>
    }
}

export const GroupMembers = ({group, children, onlyValid=true, onlyInvalid=false}) => {
    let memberships = group?.memberships || []
    if (onlyInvalid) {
        memberships = memberships.filter(
            (m) => m.valid === false
        )
    } else {
        memberships = memberships.filter(
            (m) => m.valid === onlyValid
        )
    }

    return (
        <>
            {memberships.map(
                (m, index) => <GroupMember key={m.id} group={group} membership={m}> </GroupMember>
            )}
            {children}
        </>
    )
}