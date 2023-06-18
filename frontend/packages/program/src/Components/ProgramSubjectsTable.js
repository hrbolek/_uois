import { Link } from "@uoisfrontend/shared"
import { Table } from "react-bootstrap"



export const ProgramSubjectsTableHeader = ({program}) => {
    return (
        <thead>
            <tr>
                <th>#</th>
                <th>Název</th>
                <th></th>
            </tr>
        </thead>
    )
}

export const ProgramSubjectTableRow = ({program, subject}) => {
    return (
        <tr>
            <td>{subject.name}</td>
            <td><Link tag="subject" id={subject.id}>{subject.name}</Link></td>
            <td>{subject.name}</td>
        </tr>
    )
}

export const ProgramSubjectsTableBody = ({program}) => {
    const subjects = program?.subjects || []
    return (
        <tbody>
            {subjects.map(
                (subject, index) => <ProgramSubjectTableRow key={subject.id} subject={subject} program={program} />
            )}
        </tbody>
    )
}

export const ProgramSubjectsTable = ({program}) => {
    return (
        <Table>
            <ProgramSubjectsTableHeader program={program} />
            <ProgramSubjectsTableBody program={program} />
        </Table>
    )
}