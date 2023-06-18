import { useState, useCallback } from 'react';

/**
 * shared module.
 * @module shared/components
 */

/**
 * This is Delete Button with confirmation (two state button). To get onClick response, user must click twice
 * @function
 * @param {JSX.Element[]} props.children This is usually an Icon (like the trash icon from boostrap icons)
 * @param {callback} props.onClick is called when user confirms the action by clicking secondary on red button
 * @returns JSX.Element
 */
export const DeleteButton = ({children, onClick}) => {

    //vnitrni stavova promenna definujici, zda je cervene tlacitko zobrazene nebo neni
    const [ state, setState ] = useState(0)

    //nastavi, ze se cervene tlacitko nezobrazuje
    const setState0 = useCallback(() => setState(0))

    //nastavi, ze se cervene tlacitko zobrazuje
    const setState1 = useCallback(() => setState(1))

    if (state === 0) {
        //cervene tlacitko nema byt zobrazeno
        return (
            <button className='btn btn-sm btn-warning' onClick={setState1}>{children}</button>
        )
    } else {
        //cervene tlacitko ma byt zobrazeno
        return (
            <>
                <button className='btn btn-sm btn-warning' onClick={setState0}>{children}</button>
                <button className='btn btn-sm btn-danger' onClick={onClick}>{children}</button>
            </>
        )
    }
}