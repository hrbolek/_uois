import Card from "react-bootstrap/Card";

import { Tree, TreeNode } from 'react-organizational-chart';

import { GroupSmall } from "./links";

const groupTypes = {
    "cd49e152-610c-11ed-9f29-001a7dda7110": {label: "univ", "color": 'rgb(230, 255, 230)'},
    "cd49e154-610c-11ed-bdbf-001a7dda7110": {label: "ustav", "color": 'rgb(230, 255, 255)'},
    "cd49e153-610c-11ed-bf19-001a7dda7110": {label: "fakulta", "color": 'rgb(255, 255, 230)'},
    "cd49e155-610c-11ed-bdbf-001a7dda7110": {label: "centrum", "color": 'rgb(255, 230, 255)'},
    "cd49e155-610c-11ed-844e-001a7dda7110": {label: "katedra", "color": 'rgb(230, 255, 230)'},
}
//"cd49e153-610c-11ed-bf19-001a7dda7110"

//D3.js D3js https://blog.griddynamics.com/using-d3-js-with-react-js-an-8-step-comprehensive-manual/



const createMaster = (group) => { 
    //console.log('createMaster', group.mastergroup)
    const mastergroup = group.mastergroup
    if (mastergroup) {
        const MasterComponent = createMaster(mastergroup)
        return (props) => (
            <MasterComponent>
                <TreeNode label={<div style={{'backgroundColor': groupTypes[group.grouptype.id]?.color, 'border': '1px solid black', 'padding': '5px'}}><GroupSmall group={group} /></div>}>
                    {props.children}
                </TreeNode>
            </MasterComponent>
        )
    } else {
        return (props) => (
            <Tree label={<div style={{'backgroundColor': groupTypes[group.grouptype.id]?.color, 'border': '1px solid black', 'padding': '5px'}}><GroupSmall group={group} /></div>}>
                {props.children}
            </Tree>
        )
    }
}

const Masters = ({group, children}) => {
    const MasterComponent = createMaster(group)
    return (
        <MasterComponent>
            {children}
        </MasterComponent>
    )    
}

const validAndEnabledAcademic = (groupList) => {
    return groupList.filter(g => (g.valid === "true") | (g.valid === true)).filter(g => (g.grouptype?.id in groupTypes))
}

const BuildAcademicMasterNode = ({group}) => {
    const validSubgroups = validAndEnabledAcademic(group.subgroups || [])
    const children = validSubgroups.map( g => <BuildTree key={g.id} group={g} />)
    return (
        
        <Masters group={group}>
            {children}
        </Masters>    

    )
}

const validAndEnabled = (groupList) => {
    return groupList.filter(g => (g.valid === "true") | (g.valid === true)).filter(g => !(g.grouptype?.id in groupTypes))
}
//groupTypes[group.grouptype.id]
const BuildTree = ({group}) => {
    const validSubgroups = validAndEnabled(group.subgroups || [])
    const children = validSubgroups.map( g => <BuildTree key={g.id} group={g} />)
    return(
        <TreeNode label={<div style={{'backgroundColor': groupTypes[group.grouptype.id]?.color, 'border': '1px solid black', 'padding': '5px'}}><GroupSmall group={group} /></div>}>
            {children}
        </TreeNode>
    )
}

const BuildMasterNode = ({group}) => {
    const validSubgroups = validAndEnabled(group.subgroups || [])
    const children = validSubgroups.map( g => <BuildTree key={g.id} group={g} />)
    return (

            <Masters group={group}>
                {children}
            </Masters>    
    )
}

const studyGroupType = 'cd49e157-610c-11ed-9312-001a7dda7110';
//const studyGroupMatcher = /^[1-3][1-5]\-[1-5]([A-Z]+)/gm
const studyGroupMatcher = /^(?:[1-3][1-5]\-[1-5]([^\- ]+))|(?:(OK))|(?:[1-3][1-9]\-(9))/
//const studyGroupMatcher = /^[1-3][1-5]\-[1-5]([^\- ]+)/

/*
console.log('regex test')
console.log(studyGroupMatcher.exec('23-5LTZ'))
console.log(studyGroupMatcher.exec('23-5VP Seminář A'))
console.log('regex test')
*/
const validAndStudyGroup = (groupList) => {
    return groupList.filter(g => (g.valid === "true") | (g.valid === true)).filter(g => (g.grouptype?.id == studyGroupType))
}


const BuildChainTree = ({groups}) => {
    const [first, ...others] = groups
    return (
        <TreeNode label={<div style={{'backgroundColor': null, 'border': '1px solid black', 'padding': '5px'}}><GroupSmall group={first} /></div>}>
            {others.length === 0?
                null:
                <BuildChainTree groups={others} />
            }
        </TreeNode>
    )
}

const KeyedGroups = ({sign, groups}) => {
    const groupsCopy = [...groups]
    groupsCopy.sort((a, b) => a.name > b.name)

    if (groupsCopy.length === 1) {
        return (<BuildChainTree groups={groupsCopy} />)
    } else {
        return (
            <TreeNode label={<div style={{'backgroundColor': null, 'border': '1px solid black', 'padding': '5px'}}>{sign}</div>}>
                <BuildChainTree groups={groupsCopy} />
            </TreeNode>
        )
    }
}

const BuildStudyGroupMasterNode = ({group}) => {
    const validSubgroups = group.subgroups
    //console.log(group.subgroups)
    const childrenMap = {}
    validSubgroups.forEach(g => { 
        const reMatch = studyGroupMatcher.exec(g.name)
        if (reMatch) {
            const signs = reMatch.filter(value => value)
            const sign = signs[signs.length-1]
            //console.log('reMatch', reMatch, signs, g.name)
            //const sign = reMatch[0]
            if (!(sign in childrenMap)) {
                childrenMap[sign] = []
            }
            childrenMap[sign].push(g)
        } else {
            //console.log(reMatch, g.name)
            childrenMap[g.name] = [g]
        }
    });
    //console.log(childrenMap)
    const signs = Object.keys(childrenMap)
    return(

        <Masters group={group}>
            {signs.map( 
                (sign) => <KeyedGroups key={sign} sign={sign} groups={childrenMap[sign]} />
            )}
        </Masters>    
    )
}


export const GroupSchema = (props) => {
    const group = props.group
    const academicGroups = validAndEnabledAcademic(group.subgroups || [])
    const studyGroups = validAndStudyGroup(group.subgroups || [])
    //console.log(studyGroups)
    const others = [];
    (group.subgroups || []).forEach(
        (g) => {
            const isAcademic = academicGroups.some(item => item.id === g.id)
            const isStudy = studyGroups.some(item => item.id === g.id)
            if (!((isAcademic) | (isStudy))) {
                others.push(g)
            }
        }
        
    )
    //const validSubgroups = validAndEnabled(group.subgroups || [])
    //const children = validSubgroups.map( g => <BuildTree key={g.id} group={g} />)
    return (
        <Card>
            <Card.Header>
                <Card.Title>
                    Organizační schéma
                </Card.Title>
            </Card.Header>
            <Card.Body>
                <BuildAcademicMasterNode group={{...group, subgroups: academicGroups}} /> <hr />
                <BuildMasterNode group={{...group, subgroups: others}} /> <hr />
                <BuildStudyGroupMasterNode group={{...group, subgroups: studyGroups}} /> <hr />
            </Card.Body>
        </Card>
    )
}