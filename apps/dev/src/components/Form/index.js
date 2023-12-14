import { CardCapsule } from "./CardCapsule";
import { DeleteButton } from "./DeleteButton";
import { EditableText } from "./EditableText";
import { Link } from "./Link";
import { TextInput } from "./TextInput";
// import { DroneAttributeList } from "./DroneAttributes";
// import { DroneRemoveFromMission } from "./DroneRemoveFromMission";
// import { DroneSensorsCard } from "./DroneSensors";

export default Object.assign(CardCapsule, {
    Card: CardCapsule,
    DeleteButton: DeleteButton,
    TextInput: TextInput,
    EditableText: EditableText,
    Link
})