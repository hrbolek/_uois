import { createSlice } from '@reduxjs/toolkit';
import { v1 as uuid1 } from 'uuid';
import { CreateItem, DeleteItem } from './keyedreducers';



/**
* Kompletni rez budoucim store.
* Obsluhuje zpravy
*/
export const MsgSlice = createSlice({
   name: 'msgs',
   initialState: {},
   reducers: {
       msg_add: CreateItem,
       msg_delete: DeleteItem
   }
})

export const MsgReducer = MsgSlice.reducer
export const MsgActions = MsgSlice.actions


export const MsgAddAsyncAction = ({title, variant = "success"}) => (dispatch, getState) => {
    const msgWithId = {id: uuid1(), variant, title}
    //const id = msgWithId.id

    dispatch(MsgActions.msg_add(msgWithId))
}

export const MsgFlashAsyncAction = ({title, variant = "success"}) => (dispatch, getState) => {
    const msgWithId = {id: uuid1(), variant, title}
    //const id = msgWithId.id

    dispatch(MsgActions.msg_add(msgWithId))
    setTimeout(
        () => dispatch(MsgActions.msg_delete(msgWithId)), 5000
    )
}