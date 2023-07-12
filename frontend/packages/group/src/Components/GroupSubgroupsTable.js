import { Link, TextInput } from "@uoisfrontend/shared"
import { Table } from "react-bootstrap"
import { People, PeopleFill } from "react-bootstrap-icons"

export const GroupSubgroup = ({group, subgroup, children}) => {
    return (
        <>
            <span className="btn btn-outline-success">
                <Link id={subgroup.id} tag="group"><PeopleFill /> {subgroup.name}</Link>
            </span>
            {children}
        </>
    )
}

/**
 * 
 * @param {Array} a array which going trought 
 * @param {Function} f returns [key, value] for a particular array item
 * @returns dictionary of arrays which represent subarrays of parameter a splitted by keys
 */
const pivotmap = (a, f) => {
    let result = {}
    a.forEach(
        i => {
            let [key, value] = f(i)
            console.log(key)
            if (key in result) {
                result[key].push(value)
            } else {
                result[key] = [value]
            }            
        }
    )
    return result
}

const GroupTableRow = ({group, children}) => { 
    return (
        <tr>
            <td><Link tag="group" id={group.id}>{group.name}</Link></td>
            <td>{group?.grouptype?.name}</td>
            {children}
        </tr>
    )

}
const GroupSubgroupsTableRows = ({groups, children}) => {
    return (
        <>
            {groups.map(group => <GroupTableRow key={group.id} group={group}/>)}
        </>
    )
}

export const GroupSubgroupsTable = ({group, children}) => {
    const subgroups = group?.subgroups || []
    const subgroupsIndex = pivotmap(subgroups, s => [s?.grouptype.name || "", s])
    return (
        <Table size="sm" striped bordered> 
            <thead>
                <tr>
                    <th>Název</th>
                    <th>Typ</th>
                </tr>
            </thead>
            <tbody>
            {Object.entries(subgroupsIndex).flatMap( 
                ([key, subgs]) => <GroupSubgroupsTableRows key={key} groups={subgs} />
            )}
            </tbody>

            <tfoot>
                <tr>
                    <th><TextInput /></th>
                    <th><TextInput /></th>
                </tr>
                <tr>
                    <th colSpan={2}>
                        <div className="input-group">
                            <TextInput />
                            <TextInput />
                            <button className="form-control btn btn-warning">Add</button>
                        </div>
                    </th>
                    
                </tr>
            </tfoot>

{/* 
            {subgroups.map(
                (subgroup, index) => <GroupSubgroup key={subgroup.id} group={group} subgroup={subgroup}> </GroupSubgroup>
            )} */}
            {children}
            {/* {JSON.stringify(subgroupsIndex)} */}
        </Table>
    )
}