import { useState, useMemo, useCallback } from 'react'

import { CreateDelayer } from './CreateDelayer';
import Button from 'react-bootstrap/Button';
import InputGroup from 'react-bootstrap/InputGroup';
import { PenFill, Check, X } from 'react-bootstrap-icons';
import { TextInput } from './TextInput';

/**
 * shared module.
 * @module shared/components
 */

/**
 * text paired with edit button (pencil) which changes appereance into input control (input type="text") change must be confirmed 
 * @function
 * @param {*} props.id mandatory identification, often related to id of entity 
 * @param {str} props.value value of input
 * @param {str} props.placeholder value of help if the text is not displayed
 * @param {callback} props.onChange delayed callback notifying about the change
 * @returns JSX.Element
 */
export const EditableText = ({id, value, onChange, placeholder}) => {
    const [localValue, setLocalValue] = useState(value)
    const [editable, setEditable] = useState(false)

    const localOnAllowEdit = useCallback(
        () => {
            setEditable(true)
        }, []//[id, onChange]
    )
    const checkClick = //useCallback(
        () => {
            // console.log("EditableText.checkClick A", localValue)
            setEditable(false)
            if (onChange) {
                onChange(localValue)
            }
        }
        //, []//[id, onChange])
    const crossClick = //useCallback(
        () => {
            // console.log("EditableText.crossClick A", localValue)
            // setEditable(isEditable => false)
            // setLocalValue(oldValue => value)
            setEditable(false)
            setLocalValue(value)
        }
        //, []//[id, onChange])
    const onLocalChange = (newValue) => {
        // console.log("EditableText.onLocalChange A", localValue)
        // console.log("EditableText.onLocalChange B", newValue)
        setLocalValue(newValue)
    }
    // console.log('EditableText.current_value', localValue)

    return (
        editable ? 
            <InputGroup>
                <TextInput id={id} value={value} placeholder={placeholder} onChange={onLocalChange} />
                <Button size="sm" variant='outline-warning' onClick={crossClick}><X /></Button>
                <Button size="sm" variant='outline-danger' onClick={checkClick}><Check /></Button>
            </InputGroup> : 
            <>{value} <Button size="sm" variant='outline-warning' onClick={localOnAllowEdit}><PenFill/></Button></>
        // <input className="form-control" placeholder={placeholder} value={localValue} onChange={localOnChange}/>
    )
}