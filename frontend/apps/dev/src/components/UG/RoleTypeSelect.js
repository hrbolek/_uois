import { RoleTypesQueryQuery } from "queries/UG/RoleTypesQuery"
import { useEffect, useState } from "react"

export const RoleTypeSelect = ({roletypes, onSelect}) => {
    const onChange = (e) => {
        const value = e.target.value
        console.log("RoleTypeSelect", JSON.stringify(value))
        const roletype = roletypes.find( r => r.id===value)
        if (onSelect) {
            onSelect(roletype)
        }
    }

    return (
        <select className="form-control" onChange={onChange} >
            <option>...</option>
            {roletypes.map(
                role => <option key={role.id} value={role.id}>{role.name}</option>
            )}
        </select>
    )
}

export const RoleTypeSelectFetch = ({onSelect}) => {
    const localOnSelect = (roletype) => {
        console.log("RoleTypeSelectFetch", roletype)
        if (onSelect) {
            onSelect(roletype)
        }
    }

    const [roletypes, setroletypes] = useState([])

    useEffect(
        () => {
            RoleTypesQueryQuery()
            .then(response => response.json())
            .then(json => {
                const roletypes = json?.data?.result
                if (roletypes) {
                    setroletypes(roletypes)
                } else {

                }
            })
        }, []
    )


    return (
        <RoleTypeSelect roletypes={roletypes} onSelect={localOnSelect} />
    )
}