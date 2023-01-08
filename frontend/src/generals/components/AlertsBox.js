
import { useState } from 'react'

export const Alert = (props) => {
    const { id, main, explain, type, onClose } = props
    const [visible, setVisible] = useState(true)
    const localClose = () => {
        setVisible(false)
        if (onClose) {
            onClose(id)
        }
    }

    if (type === 'alert-success') {
        setTimeout(localClose, 5 * 1000);
    }
    const clickChain = (a, b) => () => {
        a()
        b()
    }
    let extraButtons = null
    if (props.extraButtons) {
        extraButtons = props.extraButtons.map( 
            extraButton => <span key={extraButton.label}><button data-bs-dismiss="alert" {...extraButton.props} onClick={clickChain(localClose, extraButton.onClick)}>{extraButton.label}</button> </span>
        )
    }
    if (visible) {
        return (
            <div className={"alert alert-dismissible fade show " + type} role="alert">
                <strong>{main}</strong> {explain + " "} 
                {extraButtons}
                <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close" onClick={localClose}></button>
            </div>
    )} else {
        return <></>
    }
}

export const AlertsBox = (props) => {
    const { alerts, onClose } = props
    const localClose = (id) => {
        if (onClose) {
            onClose(id)
        }
    }
    return (
        <div>
            {alerts.map(
                (alert) => <Alert key={alert.id} {...alert} onClose={localClose} />
            )}
        </div>
    )
}