import { ItemComponent } from ".."

export const Items = ({items, mode}) => {
    return (
        <>
            {items.map(
                item => {
                    const Component = ItemComponent(item)
                    return <Component key={item.id} item={item} mode={mode}/>
                }
            )}
        </>
    )
}

export const Part = ({part, mode}) => {
    const items = part?.items || []
    return (
        <>
        <h4>{part.name}</h4>
        <Items items={items} mode={mode} />
        <hr />
        </>
    )
}