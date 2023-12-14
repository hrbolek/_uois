import { CardCapsule } from "./CardCapsule"
import { Link } from "../links"

export const Demo = () => {
    return (
        <CardCapsule title={"Demo links"}>
            <Link tag="user" id="2d9dc5ca-a4a2-11ed-b9df-0242ac120003">John Newbie</Link> <br />
            <Link tag="group" id="2d9dcd22-a4a2-11ed-b9df-0242ac120003">Uni</Link> <br />
            <Link tag="event" id="45b2df80-ae0f-11ed-9bd8-0242ac110002">Event</Link> <br />
            <Link tag="facility" id="66275ffa-a7b3-11ed-b76e-0242ac110002">Facility</Link> <br />
            <Link tag="survey" id="910d54a9-7f2e-41ca-b811-3c600ef82fda">Survey</Link> <br />
        </CardCapsule>
    )
}
