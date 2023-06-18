import { Part } from "./Part"

export const Parts = ({parts, mode}) => {
    return (
        <>
            {parts.map(
                part => <Part key={part.id} part={part} mode={mode} />
            )}
        </>
    )
}
export const Section = ({section, mode}) => {
    const parts = section?.parts || []

    return (
        <Parts parts={parts} mode={mode} />
    )
}