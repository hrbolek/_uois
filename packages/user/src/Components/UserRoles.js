import { Link } from '@uoisfrontend/shared';
import InputGroup from 'react-bootstrap/InputGroup';

export const UserRole_ = ({user, role, children}) => {
    const group = role?.group || {name: "unknown group"}
    const type = role?.roletype || {name: "unknown role type"}
    return (
        <>
        <InputGroup className="mb-3">
            <InputGroup.Text id="basic-addon3">
                <Link id={group?.id} tag='group'>
                {group.name}
                </Link>
            </InputGroup.Text>
            <InputGroup.Text id="basic-addon3">
                {type.name}
            </InputGroup.Text>
            {children}
        </InputGroup>
        </>
    )
}

export const UserRole = ({user, role, children}) => {
    const group = role?.group || {name: "unknown group"}
    const type = role?.roletype || {name: "unknown role type"}
    return (
        <>
            {type.name}
            {" / "}
            <Link id={group?.id} tag='group'>
                {group.name}
            </Link>
            {"  "}
            {children}
        </>
    )
}

/**
 * 
 * @param {Object} props.user 
 * the user who will be visualized
 * 
 * @param {JSX.Element[]} props.children
 * Elements which will be append to the end of visualization
 * 
 * @returns JSX.Element
 */
export const UserRoles = ({user, children}) => {
    const roles = user?.roles || []
    return (
        <>
            <b>Role </b>
            {roles.map(
                (role, index) => <UserRole key={role?.id} role={role} user={user} />
            )}
            {children}
        </>
    )
}