import { Link } from '@uoisfrontend/shared'
import Table from 'react-bootstrap/Table'

export const FacilitySubfacilitiesTableHeader = ({index, facility}) => {
    return (
        <thead>
            <tr>
                <th>#</th>
                <th>Název</th>
            </tr>
        </thead>
    )
}

export const FacilitySubfacilitiesTableRow = ({index, facility}) => {
    return (
        <tr>
            <td>{index}</td>
            <td><Link tag="facility" id={facility.id}>{facility.name}</Link></td>
        </tr>
    )
}

export const FacilitySubfacilitiesTable = ({facility}) => {
    const subfacilities = facility?.subFacilities || []
    console.log(subfacilities)
    if (subfacilities.length === 0) {
        return null
    }
    return (
        <Table size='sm' bordered striped>
            <FacilitySubfacilitiesTableHeader facility={facility} />
            <tbody>
                {subfacilities.map(
                    (f, index) => <FacilitySubfacilitiesTableRow key={f.id} index={index+1} facility={f} />
                )}
            </tbody>
        </Table>
    )
}