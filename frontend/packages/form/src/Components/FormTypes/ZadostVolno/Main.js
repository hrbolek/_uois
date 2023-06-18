import Card from "react-bootstrap/Card"
import { StudentSection } from "./StudentSection"
export const Main = ({form}) => {
    const sections = form?.sections || []
    return (
        <Card>
            <Card.Header>
                <Card.Title>Žádost o volno</Card.Title>
            </Card.Header>
            <Card.Body>
                {sections.length > 0 ? <StudentSection section={sections[0]} />: ""}
            </Card.Body>
            <Card.Footer>
                {JSON.stringify(form)}
            </Card.Footer>
        </Card>
    )
}