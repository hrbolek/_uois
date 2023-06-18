import { useState } from "react"
import { PlusLg, CheckLg } from "react-bootstrap-icons"

export const AddRemoveButton = ({state, onChangeValue}) => {
    const [_state, setState] = useState(state)
    const set0 = () => setState(0)
    const settrueCall = () => {
        setState(true)
        if (onChangeValue) {
            onChangeValue(true)
        }
    }
    const setfalse = () => setState(false)
    const setfalseCall = () => {
        setState(false)
        if (onChangeValue) {
            onChangeValue(false)
        }
    }
    switch(_state) {
        case true:
            return (
                <span className="btn btn-sm btn-outline-success" onClick={setfalseCall}><CheckLg /></span>
            )  
        case false:
            return (
                <span className="btn btn-sm btn-outline-light" onClick={set0}><PlusLg /></span>
            )
        default:
            return (
                <>
                <span className="btn btn-sm btn-outline-light" onClick={setfalse}><PlusLg /></span>
                <span className="btn btn-sm btn-outline-danger" onClick={settrueCall}><PlusLg /></span>
                </>
            )            
      } 
}