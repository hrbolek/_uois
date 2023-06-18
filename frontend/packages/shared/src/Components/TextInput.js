import { useState, useMemo, useCallback } from 'react'

import { CreateDelayer } from './CreateDelayer'

/**
 * shared module.
 * @module shared/components
 */

/**
 * input control (html input input type="text"), callback is delayed
 * 
 * @function
 * 
 * @param {*} props.sid mandatory identification, often related to id of entity 
 * 
 * @param {str} props.value value of input
 * 
 * @param {str} props.placeholder value of help if the text is not displayed
 * 
 * @param {function} props.onChange delayed callback notifying about the change
 * 
 * @returns JSX.Element
 */
export const TextInput = ({id, value, onChange, placeholder}) => {
    const [localValue, setLocalValue] = useState(value)

    const delayer = useMemo(
        () => CreateDelayer(), [id]
    )

    const localOnChange = //useCallback(
        (e) => {
            const newValue = e.target.value
            setLocalValue(newValue)
            if (onChange) {
                delayer(() => onChange(newValue))
            }
            //console.log("TextInput", newValue)
        }
        //, [id, onChange])
    const onBlur = //useCallback(
        (e) => {
            const newValue = e.target.value
            if (newValue !== localValue) {
                //console.log("onFocusOut")
                localOnChange(e)
                onChange(newValue)
            }
        }
        //, [id, onChange])

    return (
        <input className="form-control" placeholder={placeholder} value={localValue} onChange={localOnChange} onBlur={onBlur}/>
    )
}