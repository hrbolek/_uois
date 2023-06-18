import Card from "react-bootstrap/Card"
import { Section } from "./Section"
import { Row } from "react-bootstrap"
import { useState } from "react"

export const Sections = ({sections, mode}) => {
    return (
        <>
            {sections.map(
                section => <Section key={section.id} section={section} mode={mode}/>
            )}
        </>
    )
}
export const Main = ({form, mode}) => {
    const sections = form?.sections || []
    return (
        <Card>
            <Card.Header>
                <Card.Title>{form?.name}</Card.Title>
            </Card.Header>
            <Card.Body>
                <Sections sections={sections} mode={mode}/>
            </Card.Body>
            <Card.Footer>
                {JSON.stringify(form)}
            </Card.Footer>
        </Card>
    )
}

export const MainTabs = ({active, sections, mode, onChange}) => {
    const onChange_ = (selectedKey) => {
        if (onChange) {
            onChange(selectedKey)
        }
    }
    return(
        <>
            {sections.map(
                section => (section.id === active)?
                <button key={section.id} 
                    className="btn btn-success" onClick={() => onChange_(section.id)}>
                        {section.name}
                </button>:
                <button key={section.id} 
                    className="btn btn-outline-success" onClick={() => onChange_(section.id)}>
                        {section.name}
                </button>
            )}
        </>
        
    )
}


export const MainTabbed = ({form, mode}) => {
    const sections = form?.sections || []
    const [section, setSection] = useState(sections[0])
    const onChange = (id) => {
        const section = sections.find( s=> s.id === id)
        setSection(section)
    }
    return (
        <Card>
            <Card.Header>
                <Card.Title>{form?.name}</Card.Title>
            </Card.Header>
            <Card.Body>
                {
                section?<>
                    <MainTabs sections={sections} active={section.id} onChange={onChange}/>
                    <Sections sections={[section]} mode={mode}/>
                </>: ""
                }
                
            </Card.Body>
            <Card.Footer>
                {JSON.stringify(form)}
            </Card.Footer>
        </Card>
    )
}