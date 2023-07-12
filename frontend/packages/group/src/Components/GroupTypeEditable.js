import { EditableAttributeSelect, authorizedFetch, useFreshItem } from "@uoisfrontend/shared"
import { GroupUpdateAsyncAction } from "../Actions/GroupUpdateAsyncAction"
import All from "@uoisfrontend/shared/src/keyedreducers"

export const GroupTypesItemStoreId = "baa957a4-3453-476f-ad88-e093f0dfa47b"

export const GroupTypesQueryJSON = () => ({
    query: `{
        result: groupTypePage {
          id
          name
          nameEn
        }
      }`
})

export const GroupTypesFetchQuery = () => 
    authorizedFetch('/gql', {
        body: JSON.stringify(GroupTypesQueryJSON())
    })


export const GroupTypesFetchAsyncAction = () => (dispatch, getState) => {
    // console.log("GroupRoleUpdateAsyncAction", membership)
    return (
        GroupTypesFetchQuery()
        .then(response => response.json())
        .then(json=> {
            const result = json?.data?.result
            if (result) {
                const action = All.ItemSliceActions.item_update({id: GroupTypesItemStoreId, grouptypes: result})
                dispatch(action)
            }
            return json
        })
    )
}
    
    
export const GroupTypesOptions = () => {
    const [item] = useFreshItem({id: GroupTypesItemStoreId}, GroupTypesFetchAsyncAction)
    console.log("GroupTypesOptions", item)
    const grouptypes = item?.grouptypes
    if (grouptypes) {
        return (<>
            {grouptypes.map(
                gt => <option key={gt.id} value={gt.id}>{gt.name}</option>
            )}
        </>)
    } else {
        return null
    }
}

export const GroupTypeEditable = ({group}) => {
    return (
        <EditableAttributeSelect 
            item={group} 
            label="Typ"
            onAttributeGet={(group) => group?.grouptype?.id}
            onAttributeSet={(group, value) => ({...group, grouptypeId: value})}
            asyncUpdater={GroupUpdateAsyncAction}>
            <GroupTypesOptions />
        </EditableAttributeSelect>
    )
}