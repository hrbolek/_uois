import { useEffect, useState } from "react"
import { useSelector } from "react-redux"
import { useDispatch } from "react-redux"

/**
 * shared module.
 * @module shared/hooks
 */


const fakePromise = {
    then: (json) => new Promise((resolve, reject) => null),
    finally: (json) => new Promise((resolve, reject) => null),
    catch: (json) => new Promise((resolve, reject) => null)
}
const fakePromise_ = Promise.resolve(null)

/**
 * @function
 * @param {*} oldItemWithId Object with attribute id
 * @param {function} AsyncAction async function to be executed and which returns incomming data (json)
 * @returns [data, Promise(thenable)]
 */
export const useFreshItem = ({id}, AsyncAction) => {
    //const id = oldItemWithId.id
    // console.log("useFreshItem", id)
    const dispatch = useDispatch()
    const items = useSelector(state => state.items)
    if (!items) {
        throw Error("bad use of store and useFreshItem hook, checks that store state has items attribute")
    }
    const result = items[id]
    // console.log("useFreshItem", id, result)
    const [resultPromise, setPromise] = useState(fakePromise)

    useEffect(
        () => {
            const controller = new AbortController();
            const signal = controller.signal;
        
            const presult = dispatch(AsyncAction({id}, signal))
            setPromise(prev => presult)

            // return () => {
            //     controller.abort()
            // }
        },
        [id, AsyncAction, dispatch]
    )
    return [result, resultPromise]
}

export const useFreshItem_ = ({id}, AsyncAction) => {
    //const id = oldItemWithId.id
    const dispatch = useDispatch()
    const items = useSelector(state => state.items)
    const result = items[id]

    // const [resultPromise, setPromise] = useState(fakePromise)

    
    return [result, dispatch(AsyncAction({id}))]
}