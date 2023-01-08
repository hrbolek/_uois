import { useCallback, useState } from "react"

export const ExpandableButton = (props) => {
    const [visible, setVisible] = useState(false)

    const setFalse = useCallback(() => setVisible(false), [setVisible])
    const setTrue = useCallback(() => setVisible(true), [setVisible])

    if (visible) {
        return (
            <button onMouseOver={setTrue} onMouseOut={setFalse} className={props.className}>{props.children}</button>
        )
    } else {
        return (
            <button onMouseOver={setTrue} onMouseOut={setFalse} className={props.className}>{props.children[0][0]}</button>
        )
    }
}