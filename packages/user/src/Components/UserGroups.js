import { Link } from '@uoisfrontend/shared';
import InputGroup from 'react-bootstrap/InputGroup';

export const UserGroup_ = ({user, group, children}) => {
    const grouptypename = group?.type?.name
    return (
        <>
            <InputGroup className="mb-3">
                <InputGroup.Text id="basic-addon3">
                    <Link id={group?.id} tag="group">
                    {group?.name}
                    </Link>
                </InputGroup.Text>
                {children}
            </InputGroup>
        </>
    )
}

export const UserGroup = ({user, group, children}) => {
    const grouptypename = group?.type?.name
    return (
        <>
            {grouptypename}
            <Link id={group?.id} tag="group">
                {group?.name} 
            </Link>
            {" "}
            {children}
        </>
    )
}

/**
 * @function 
 * 
 * @param {Object} props.user 
 * an user who's groups will be shown, the memberships is defined by membership array
 * 
 * @param {JSX.Element[]} props.children 
 * elements which will be added to the end of visualization
 * 
 * @param {boolean} props.onlyValid 
 * if set to true, and onlyInvalid is not true only valid memberships will be used for group visualization
 * 
 * @param {boolean} props.onlyInvalid 
 * if set to true, only invalid memberships will be used for group visualization
 * 
 * @returns JSX.Element
 */
export const UserGroups = ({user, children, onlyValid=true, onlyInvalid=false}) => {
    let membership = user?.membership || []
    // console.log(membership)
    if (onlyInvalid) {
        membership = membership.filter(
            m => m?.valid === false
        )    
    } else {
        membership = membership.filter(
            m => m?.valid === onlyValid
        )    
    }
    // console.log(membership)
    return (
        <>  <b>Členství </b>
            {membership.map(
                (m, index) => <UserGroup key={m.id} user={m?.user} group={m?.group} />
            )}
            {children}
        </>
    )
}