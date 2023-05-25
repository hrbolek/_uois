import { useState, useCallback } from 'react';

/**
 * This is Delete Button with confirmation (two state button).
 * @param {*} children
 * @param {() => void} onClick
 * @returns 
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