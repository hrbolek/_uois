import { ItemComponent } from ".."  
export const Student_01_Part = ({part}) => {
    const items = part?.items || []
    return (
        <>
        
        <h3>{part.name}</h3>
        {items.map(
            item => {
                const Component = ItemComponent(item)
                return <Component key={item.id} item={item} />
            }
        )}
        {JSON.stringify(part)}
        </>
    )
}