import { useDispatch } from "react-redux"
import { EditableText } from "./EditableText"
import { CheckGQLError, MsgFlashAction } from "../.."

/**
 * shared module.
 * @module shared/components
 */

/**
 * @function
 * @param {Object} props.item item to be edited
 * @param {Object[]} props.children would be list of <option />
 * @param {callback} props.onAttributeGet function which should get the current vaule of attribute
 * @param {callback} props.onAttributeSet function which creates a new instance of item and which would be passed to asyncUpdater
 * @param {function(item): Promise} props.asyncUpdater
 * @returns JSX.Element
 */
export const EditableAttributeSelect = ({item, label, children, onAttributeGet, onAttributeSet, asyncUpdater}) => {
    const dispatch = useDispatch()
    const attributeValue = onAttributeGet(item)
    const onChange_ = (e) => {
        const value = e.target.value
        const newItem = onAttributeSet({...item}, value)
        console.log("EditableAttributeText.oldItem", item)
        console.log("EditableAttributeText.newItem", newItem)
        const action = asyncUpdater({...newItem})
        // console.log("EditableAttributeText.action", action)
        dispatch(action)
        .then(
            CheckGQLError({
                "ok": () => dispatch(MsgFlashAction({title: "Změna ok"})),
                "fail": (json) => dispatch(MsgFlashAction({title: "Něco se nepovedlo" + JSON.stringify(json)})),
            })
        )
    }
    return (
        // <EditableText id={item.id} value={attributeValue} onChange={onChange_} />
        <div className="form-floating">
            <select className="form-select" id={"select-"+item.id} value={attributeValue} onChange={onChange_} aria-label="">
                {children}
            </select>
            <label htmlFor={"select-"+item.id}>{label}</label>
        </div>
    )
}