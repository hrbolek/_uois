import { authorizedFetch } from "@uoisfrontend/shared"
import All from "@uoisfrontend/shared/src/keyedreducers"
import { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"

export const RoleTypesQueryJSON = () => ({
    query: `{
        result: roleTypePage {
          id
          name
          nameEn
        }
      }`
})

export const RoleTypesFetchQuery = () => 
    authorizedFetch('/gql', {
        body: JSON.stringify(RoleTypesQueryJSON())
    })

export const RolesItemStoreId = "bb1251d4-0c82-4428-956e-4c90d509781f"

export const RoleTypesFetchAsyncAction = () => (dispatch, getState) => {
    // console.log("GroupRoleUpdateAsyncAction", membership)
    return (
        RoleTypesFetchQuery()
        .then(response => response.json())
        .then(json=> {
            const result = json?.data?.result
            if (result) {
                const action = All.ItemSliceActions.item_update({id: RolesItemStoreId, roletypes: result})
                dispatch(action)
            }
            return json
        })
    )
}

export const RoleTypeSelect = ({ label="********", onSelect }) => {
    const items = useSelector(state => state.items)
    const dispatch = useDispatch()
    const roletypes = items[RolesItemStoreId]
    useEffect(
        () => {
            if (roletypes) {

            } else {
                dispatch(RoleTypesFetchAsyncAction())
                .then(json => json)
            }
        }
    )
    const onChange = (e) => {
        const value = e.target.value
        if (onSelect) {
            onSelect(value)
        }
    }

    if (roletypes) {
        return (
            // <div className="form-floating">
            //     <select className="form-select" onChange={onChange} id="roleselect" aria-label={label}>
            //         <option key={"role"}>--- ? ---</option>
            //         {roletypes.roletypes.map(
            //             roletype => <option key={roletype.id} value={roletype.id}>{roletype.name}</option>
            //         )}
            //     </select>
            //     <label htmlFor="roleselect">{label}</label>
            // </div>

            <div className="form-floating">
                <select className="form-select" id="roleselect" onChange={onChange} aria-label="Floating label select example">
                <option key={"role"}>--- ? ---</option>
                    {roletypes.roletypes.map(
                        roletype => <option key={roletype.id} value={roletype.id}>{roletype.name}</option>
                    )}
                </select>
                <label htmlFor="roleselect">{label}</label>
            </div>


            // <div class="form-floating">
            //     <select class="form-select" id="roleselect" aria-label="Floating label select example">
            //         <option selected>Open this select menu</option>
            //         <option value="1">One</option>
            //         <option value="2">Two</option>
            //         <option value="3">Three</option>
            //     </select>
            //     <label for="roleselect">Works with selects</label>
            // </div>
        )
    } else {
        return null
    }
};
