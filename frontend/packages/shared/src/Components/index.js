import { CardCapsule } from "./CardCapsule";
import { DeleteButton } from "./DeleteButton";
import { EditableText } from "./EditableText";
import { EditableAttributeText } from "./EditableAttributeText";
import { EditableAttributeSelect } from "./EditableAttributeSelect";
import { Link } from "./Link";
import { TextInput } from "./TextInput";

export { DatePicker } from "./DatePicker";
export { DateTimePicker } from "./DateTimePicker";

export { Dialog } from "./Dialog";
export { LoginButton, LoginPage } from './LoginButton'

// import { DroneAttributeList } from "./DroneAttributes";
// import { DroneRemoveFromMission } from "./DroneRemoveFromMission";
// import { DroneSensorsCard } from "./DroneSensors";

const Card = CardCapsule
const All = { Card, DeleteButton, TextInput, EditableText }
export { Card, DeleteButton, TextInput, EditableText, EditableAttributeText, EditableAttributeSelect }
export default All

export { Demo } from "./Demo";
