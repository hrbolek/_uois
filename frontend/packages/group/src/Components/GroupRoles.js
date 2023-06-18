import { Link } from "@uoisfrontend/shared"

export const GroupRole = ({group, role, children}) => {
    const user = role?.user || {id: "", name: "Neznámý", surname: "Neznámý", email: "@"}
    return (
        <>
            {role?.roletype?.name} <Link id={role.user.id} tag="user">{user.name} {user.surname}</Link> 
            {children}
        </>
    )
}

/**
 * Displays list of roles which have been assigned to users for this group
 * @function
 *  
 * @param {Object} props.group
 * group which roles will be visualized
 * 
 * @param {boolean} props.onlyInvalid
 * if true, only invalid roles are displayed
 * 
 * @param {boolean} props.onlyValid
 * if true, and onlyInvalid is false only valid roles are displayed
 * 
 * @returns JSX.Element
 */
export const GroupRoles = ({group, children, onlyValid=true, onlyInvalid=false}) => {
    let roles = group?.roles || []
    if (onlyInvalid) {
        roles = roles.filter(role => role.valid === false)
    } else {
        roles = roles.filter(role => role.valid === onlyValid)
    }
    return (
        <>
            {roles.map(
                    (role, index) => role?.valid ? <GroupRole key={role.id} role={role} group={group}>< br/> </GroupRole>: ""
            )}
            {children}
        </>
    )
}