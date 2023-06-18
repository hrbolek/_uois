import { Link } from "@uoisfrontend/shared"
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

export const GroupSubgroups = ({group, children}) => {
    const subgroups = group?.subgroups || []
    const subgroupsIndex = pivotmap(subgroups, s => [s?.grouptype.name || "", s])
    return (
        <> {
            Object.entries(subgroupsIndex).flatMap( ([key, subgs]) => {
                const result = subgs.map(
                    (subgroup, index) => <GroupSubgroup key={subgroup.id} group={group} subgroup={subgroup}> </GroupSubgroup>    
                )
                result.push(<hr key={"br-" + key}/>)
                return result
            }
            )
        }
{/* 
            {subgroups.map(
                (subgroup, index) => <GroupSubgroup key={subgroup.id} group={group} subgroup={subgroup}> </GroupSubgroup>
            )} */}
            {children}
            {/* {JSON.stringify(subgroupsIndex)} */}
        </>
    )
}