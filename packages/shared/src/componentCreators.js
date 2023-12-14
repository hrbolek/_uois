import { Col, Row } from "react-bootstrap"
import { TextInput } from "./Components/TextInput"
import { useEffect, useState } from "react"

export const createButton = ({asyncAction}) => {
    const Button = ({item, children, ...props}) => {
        const onClick = () => asyncAction({item})
        return (<button onClick={onClick} {...props}>{children}</button>)
    }
    return Button
}

//same as above
export const createButton_ = ({asyncAction}) => ({item, children, ...props}) =>  (<button onClick={() => asyncAction({item})} {...props}>{children}</button>)


export const createAttributeTextEditor = ({label, attributeName, asyncAction, Component=TextInput}) => {
    const AttributeEditor = ({item, ...props}) => {
        const onChange = (value) => {
            const newItem = {...item}
            newItem[attributeName] = value
            asyncAction(newItem)
        }
        return <Component label={label} id={item.id} value={item[attributeName]} onChange={onChange} {...props} />
    }
    return AttributeEditor 
}


export const SelectFloatingElement = ({value, onChange, label, options, ...props}) => {
    const htmlid = "SelectFloatingElement" + value
    const onChange_ = (e) => {
        const value = e.target.value
        if (onChange) {
            onChange(value)
        }
    }
    return (
        <div className="form-floating">
            <label htmlFor={htmlid}>{label}</label>
            <select className="form-select" id={htmlid} value={value} onChange={onChange_} aria-label={label} {...props}>
                <option key={"shouldselectsomething"}>--- ? ---</option>
                {options.map(
                    option => <option key={option.id} value={option.id}>{option.name}</option>
                )}
            </select>
        </div>
    )
}

export const SelectElement = ({value, label, onChange, options, ...props}) => {
    const htmlid = "SelectElement" + value
    const onChange_ = (e) => {
        const value = e.target.value
        if (onChange) {
            onChange(value)
        }
    }
    return (
        <select className="form-select form-select-sm" id={htmlid} value={value} onChange={onChange_} aria-label={label} {...props}>
            <option key={"shouldselectsomething"}>--- ? ---</option>
            {options.map(
                option => <option key={option.id} value={option.id}>{option.name}</option>
            )}
        </select>
    )
}

export const createAttributeSelectEditor = ({label, attributeName, asyncAction, asyncFetchItemsAction=Promise.resolve({data: {result: []}})}) => {
    const AttributeEditor = ({item, ...props}) => {
        const [options, setOptions] = useState([])
        useEffect(
            () => {
                if (options.length === 0) {
                    asyncFetchItemsAction()
                    .then(json => {
                        const result = json?.data?.result
                        if (result) {
                            setOptions(result)
                        }
                        return json
                    })
                }
            }
        )
        const onChange = (newValue) => {
            const newItem = {...item}
            newItem[attributeName] = newValue
            asyncAction(newItem)
        }
        return <SelectFloatingElement value={item[attributeName]} label={label} options={options} onChange={onChange} {...props}/>
    }
    return AttributeEditor 
}

export const createTableHeader = ({firstCell="#", mainCells=[], toolsCell=null}) => {
    const TableHeader = ({children, ...props}) => (
        <thead {...props}>
            {children}
            <tr>
                <th>{firstCell}</th>
                {mainCells.map(
                    label => <th key={label}>{label}</th>
                )}
                {
                    toolsCell?<th>{toolsCell}</th>:""
                }
            </tr>
        </thead>
    )
    return TableHeader
}

export const createTableBodyRow = ({firstCell = ({item}) => <td>{item.id}</td>, mainCells=[], toolsCell = () => <td></td>}) => {
    const FirstCellComponent = firstCell
    const ToolsCellComponent = toolsCell
    const TableRow = ({item, children, ...props}) => {
        return (
            <tr {...props}>
                <FirstCellComponent item={item} {...item}/>
                {
                    mainCells.map(Component => <Component key={Component} item={item} {...item}/>)
                }
                {
                    toolsCell? <ToolsCellComponent item={item} {...item} />: ""
                }
                {
                    children? {children} : ""
                }
            </tr>
        )
    }
    return TableRow
}

const defaultAttributeLabelColSize = 2
const defaultAttributeValueColSize = 10

export const AttributeIdComponent = ({id}) => <Row><Col md={defaultAttributeLabelColSize}>Id</Col><Col md={defaultAttributeValueColSize}>{id}</Col></Row>
export const AttributeNameComponent = ({name}) => <Row><Col md={defaultAttributeLabelColSize}>Název</Col><Col md={defaultAttributeValueColSize}>{name}</Col></Row>

export const createAttributeReadOnlyComponent = ({attributeName, label}) => ({item}) =>
    <Row><Col md={defaultAttributeLabelColSize}>{label}</Col><Col md={defaultAttributeValueColSize}>{item[attributeName]}</Col></Row>

export const createAttributeWritableComponent = ({attributeName, label}) => ({item, children}) =>
    <Row><Col md={defaultAttributeLabelColSize}>{label}</Col><Col md={defaultAttributeValueColSize}>{children}</Col></Row>

export const createAttributesSegment = (attributeComponents={
    id: AttributeIdComponent,
    name: AttributeNameComponent
}) => {
    return ({item}) => {
        <>
            {Object.entries(attributeComponents).map(
                ([label, Component]) => <Component key={label+item.id} item={item} />
            )}
        </>
    }
}

