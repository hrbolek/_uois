import { Student_01_Part } from "./Student_01_Part"

export const StudentSection = ({section}) => {
    const parts = section?.parts || []
    return (
        <>
        
        <h3>{section.name}</h3>

        <Student_01_Part part={parts[0]} />
        {JSON.stringify(section)}
        </>
    )
}