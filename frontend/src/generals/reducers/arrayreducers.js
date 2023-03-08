import merge from 'lodash.merge';

export const AddItem = (state, action) => {
    const item = action.payload;

    const result = [...state, item]
    return result
}

export const DeleteItem = (state, action) => {
    const item = action.payload;

    const result = state.filter(i => i.id !== item.id)
    return result
}

export const ReplaceItem = (state, action) => {
    const item = action.payload;
    const without = state.filter(i => i.id !== item.id)
    const result = [...without, item]
    return result
}

export const UpdateItem = (state, action) => {
    const item = action.payload;
    const _item = state.find(i => i.id === item.id)
    const mergedItem = merge(_item, item)
    const without = state.filter(i => i.id !== item.id)
    const result = [...without, mergedItem]
    return result
}